from typing import Dict, Tuple, List
from flwr.common import NDArrays, Scalar
from transformers import (
    AutoImageProcessor,
    TrainingArguments,
    Trainer,
    DefaultDataCollator,
)
from peft import (
    LoraConfig,
    LoftQConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    get_peft_model_state_dict,
)
from .armisticeai import UploadRequest

import flwr as fl
import torch
from collections import OrderedDict
import evaluate
import numpy as np
import json

from ._utils import (
    load_dataset,
    split_dataset,
    load_labels,
    load_label_id_map,
    serialize_for_pyo3,
    preprocess,
    load_model,
    optimal_chunk_length,
)
from enum import Enum
import uuid
import os
from ._exceptions import ArmisticeAIError


class TrainingType(Enum):
    FULL = 1
    LORA_FP16 = 2
    LORA_INT8 = 3
    QLORA_INT4 = 4


# Flower client
class ArmisticeAI(fl.client.NumPyClient):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        checkpoint: str | None = "google/vit-base-patch16-224-in21k",
        training_type: str = "lora_fp16",
        dataset: str,
        output_dir: str,
        batch_size: int = 16,
        r: int = 16,
        dap: bool = True,
        test_partition: bool = False,
        partition_percent: List | None = None,
        partition_index: int | None = None,
        wandb: bool | None = None,
        server_address: str | None = "127.0.0.1:8080",
    ) -> None:
        """Construct a new armisticeai client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ARMISTICEAI_API_KEY`
        - `organization` from `ARMISTICEAI_ORG_ID`
        - `project` from `ARMISTICEAI_PROJECT_ID`
        """
        if api_key is None:
            api_key = os.environ.get("ARMISTICEAI_API_KEY")
        if api_key is None:
            raise ArmisticeAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ARMISTICEAI_API_KEY environment variable"
            )
        self.api_key = api_key

        if organization is None:
            organization = os.environ.get("ARMISTICEAI_ORG_ID")
        self.organization = organization

        if project is None:
            project = os.environ.get("ARMISTICEAI_PROJECT_ID")
        self.project = project

        trainset, testset = load_dataset(dataset)
        if test_partition:
            trainset = split_dataset(trainset, partition_percent)[partition_index]
            testset = split_dataset(testset, partition_percent)[partition_index]

        self.image_processor = AutoImageProcessor.from_pretrained(
            checkpoint, device_map="auto"
        )
        self.trainset, self.testset = preprocess(
            self.image_processor, trainset, testset
        )

        self.training_type = TrainingType[training_type.upper()]

        self.client_id = uuid.uuid4()

        labels = load_labels(trainset)
        label2id, id2label = load_label_id_map(labels)

        load_in_8bit = False
        load_in_4bit = False
        if self.training_type == TrainingType.LORA_INT8:
            load_in_8bit = True

        # NOTE: Using LoftQ for now
        # if training_type == TrainingType.QLORA_INT4:
        #     load_in_4bit = True
        print(f"labels: {labels}, load_in_8_bit: {load_in_8bit}")
        self.model = load_model(
            checkpoint, labels, label2id, id2label, load_in_8bit, load_in_4bit
        )
        self.dap = dap
        if r is not None:
            alpha = 2 * r
        if (
            self.training_type == TrainingType.LORA_FP16
            or self.training_type == TrainingType.LORA_INT8
        ):
            lora_config = LoraConfig(
                r=r,
                lora_alpha=alpha,
                target_modules=["query", "value"],
                lora_dropout=0.1,
                bias="none",
                modules_to_save=["classifier"],
            )
            if self.training_type == TrainingType.LORA_INT8:
                self.model = prepare_model_for_kbit_training(self.model)
            self.model = get_peft_model(self.model, lora_config)
        elif self.training_type == TrainingType.QLORA_INT4:
            loftq_config = LoftQConfig(loftq_bits=4)
            lora_config = LoraConfig(
                init_lora_weights="loftq",
                loftq_config=loftq_config,
                r=r,
                lora_alpha=alpha,
                target_modules=["query", "value"],
                lora_dropout=0.1,
                bias="none",
                modules_to_save=["classifier"],
            )
            self.model = get_peft_model(self.model, lora_config)

        if self.training_type != TrainingType.FULL:
            print(f"Init model: {self.get_parameters({})[2][0][:10]}")
        else:
            print(f"Init model: {self.get_parameters({})[1][0][0][:10]}")

        self.data_collator = DefaultDataCollator()
        self.accuracy = evaluate.load("accuracy")
        self.output_dir = output_dir + "/client_" + str(self.client_id)
        self.batch_size = batch_size
        self.server_address = server_address

    def get_parameters(self, config: Dict[str, Scalar]) -> NDArrays:
        if self.training_type == TrainingType.FULL:
            state_dict = self.model.state_dict()
        else:
            state_dict = get_peft_model_state_dict(self.model)
        return [val.cpu().numpy() for _, val in state_dict.items()]

    def set_parameters(self, parameters):
        state_dict = self.model.state_dict()
        if self.training_type != TrainingType.FULL:
            lora_keys = get_peft_model_state_dict(self.model).keys()
            lora_dict = OrderedDict(
                {k: torch.Tensor(v) for k, v in zip(lora_keys, parameters)}
            )
            full_dict = {}
            for k in state_dict:
                if k in lora_dict:
                    full_dict[k] = lora_dict[k]
                else:
                    full_dict[k] = state_dict[k]

            self.model.load_state_dict(full_dict)
        else:
            params_dict = zip(state_dict.keys(), parameters)
            ordered_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
            self.model.load_state_dict(ordered_dict)

    def _create_trainer(self, config, eval=False):
        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            return self.accuracy.compute(predictions=predictions, references=labels)

        output_dir = self.output_dir
        local_epochs = 1
        lr = 5e-5
        fp16 = False
        if not eval:  # If training
            output_dir = self.output_dir + "/fed_round_" + str(config["server_round"])
            local_epochs = config["local_epochs"]

        if self.training_type != TrainingType.FULL:
            lr = 5e-4
            fp16 = True

        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            remove_unused_columns=False,
            num_train_epochs=local_epochs,
            evaluation_strategy="epoch",
            warmup_ratio=0.1,
            logging_steps=100,
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            learning_rate=lr,
            fp16=fp16,
            label_names=["labels"],
            report_to="none",
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=self.data_collator,
            train_dataset=self.trainset,
            eval_dataset=self.testset,
            tokenizer=self.image_processor,
            compute_metrics=compute_metrics,
        )

        if eval and (config["server_round"] == config["total_rounds"]):
            # Save the final aggregated model received from server.
            trainer.save_model(self.output_dir + "/final")

        return trainer

    def fit(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> tuple[NDArrays, int, dict[str, Scalar]]:
        self.set_parameters(parameters)
        trainer = self._create_trainer(config)
        if self.dap:
            keys_to_check = [
                "task_id",
                "dap_leader",
                "dap_helper",
                "vdaf",
                "time_precision",
            ]
            missing_keys = [key for key in keys_to_check if key not in config]
            if missing_keys:
                raise KeyError(f"Missing keys: {', '.join(missing_keys)}")
            print(f"[DAP]: task_id_encoded inside fit: {config['task_id']}")

        train_results = trainer.train()
        eval_results = trainer.evaluate()

        out = {
            "train_loss": train_results.training_loss,
            "eval_loss": eval_results["eval_loss"],
            "accuracy": eval_results["eval_accuracy"],
        }
        train_accuracy = eval_results["eval_accuracy"]
        params = self.get_parameters(config)
        if self.training_type != TrainingType.FULL:
            print(f"[TANYA] Local model after fit: {params[2][0][:10]}")
        else:
            print(f"[TANYA] Local model after fit: {params[1][0][0][:10]}")

        print(f"[TANYA] Local model accuracy: {train_accuracy}")

        if self.dap:
            measurements = serialize_for_pyo3(params)
            print(
                f"me new measure: {measurements[24576::24586]}, len: {len(measurements)}"
            )
            vdaf = json.loads(config["vdaf"])
            task_config = {
                "task_id": config["task_id"],
                "leader": config["dap_leader"],
                "helper": config["dap_helper"],
                "bits": int(vdaf["bits"]),
                "length": len(measurements),
                "chunk_length": optimal_chunk_length(
                    len(measurements) * int(vdaf["bits"])
                ),
                "time_precision": config["time_precision"],
            }
            req = UploadRequest(task_config, measurements)
            _ = req.run()
            return [], len(self.trainset), out  # TODO

        return params, len(self.trainset), out

    def evaluate(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        self.set_parameters(parameters)
        if self.training_type != TrainingType.FULL:
            print(
                f"[TANYA] Remote model received for eval: {self.get_parameters({})[2][0][:10]}"
            )
        else:
            print(
                f"[TANYA] Remote model received for eval: {self.get_parameters({})[1][0][0][:10]}"
            )

        trainer = self._create_trainer(config, True)
        results = trainer.evaluate()
        eval_loss = results["eval_loss"]
        eval_accuracy = results["eval_accuracy"]
        print(f"[TANYA] Remote model eval_loss: {eval_loss}, accuracy: {eval_accuracy}")

        return (
            results["eval_loss"],
            len(self.testset),
            {"accuracy": results["eval_accuracy"]},
        )

    def train(self) -> None:
        fl.client.start_client(
            server_address=self.server_address,
            client=self.to_client(),
            grpc_max_message_length=2147483647,  # 2GB
        )
