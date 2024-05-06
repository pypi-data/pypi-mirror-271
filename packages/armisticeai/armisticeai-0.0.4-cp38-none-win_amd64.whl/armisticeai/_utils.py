from transformers import AutoModelForImageClassification, BitsAndBytesConfig
from datasets import (
    load_dataset as load_dataset_hf,
    load_from_disk,
    Dataset,
    load_dataset_builder,
)
import random
from torchvision.transforms import v2
import torch
from typing import Any, List, Tuple
import os
from ._exceptions import ArmisticeAIError

import numpy as np
import numpy.typing as npt
import math

NDArray = npt.NDArray[Any]
NDArrays = List[NDArray]
SerializedParameters = List[bytes]


def split_dataset(ds: Dataset, percentages: list) -> list:
    total_size = len(ds)
    split_sizes = [int(p * total_size) for p in percentages]

    # Adjust the last split size to account for rounding errors
    split_sizes[-1] = total_size - sum(split_sizes[:-1])

    # Shuffle indices to ensure random splits
    random.seed(42)
    indices = list(range(total_size))
    random.shuffle(indices)

    split_datasets = []
    curr_idx = 0
    for size in split_sizes:
        split_indices = indices[curr_idx : curr_idx + size]
        split_dataset = ds.select(split_indices)
        split_datasets.append(split_dataset)
        curr_idx += size

    return split_datasets


def load_dataset(name: str) -> Tuple[Dataset, Dataset]:
    if os.path.isdir(name):
        dataset = load_from_disk(name)
    else:
        try:
            load_dataset_builder(name, token=True)
        except:
            raise ArmisticeAIError(
                f"Failed to load dataset from HuggingFace with identifier '{name}'"
            )
    dataset = load_dataset_hf(name, token=True)
    return dataset["train"], dataset["validation"]


def preprocess(image_processor, trainset, testset):
    _transforms = v2.Compose(
        [
            v2.RandomResizedCrop(
                (image_processor.size["height"], image_processor.size["width"])
            ),
            v2.ToImage(),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(
                mean=image_processor.image_mean, std=image_processor.image_std
            ),
        ]
    )

    def transforms(examples):
        examples["pixel_values"] = [
            _transforms(img.convert("RGB")) for img in examples["image"]
        ]
        del examples["image"]
        return examples

    return trainset.with_transform(transforms), testset.with_transform(transforms)


def load_labels(trainset: Dataset):
    return trainset.features["label"].names


def load_label_id_map(labels):
    label2id, id2label = dict(), dict()
    for i, label in enumerate(labels):
        label2id[label] = i
        id2label[i] = label
    return label2id, id2label


def load_model(
    checkpoint, labels, label2id, id2label, load_in_8bit=False, load_in_4bit=False
):
    if load_in_8bit or load_in_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=load_in_8bit, load_in_4bit=load_in_4bit
        )
    else:
        bnb_config = None

    return AutoModelForImageClassification.from_pretrained(
        checkpoint,
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
        quantization_config=bnb_config,
        device_map="auto",
    )


def serialize_for_pyo3(ndarrays: NDArrays):
    # flatten
    flattened = [arr.ravel() for arr in ndarrays]

    # rescale
    original_range = (-1, 1)
    target_range = (0, 2**32 - 1)
    rescaled = [
        np.interp(arr, original_range, target_range)
        .astype(np.uint32)
        .astype(str)
        .tolist()
        for arr in flattened
    ]

    # flatter
    flat = [item for sublist in rescaled for item in sublist]

    return flat


def optimal_chunk_length(measurement_length):
    if measurement_length <= 1:
        return 1

    class Candidate:
        def __init__(self, gadget_calls, chunk_length):
            self.gadget_calls = gadget_calls
            self.chunk_length = chunk_length

    max_log2 = math.floor(math.log2(measurement_length + 1))
    best_opt = min(
        (
            Candidate(
                (1 << log2) - 1,
                (measurement_length + (1 << log2) - 2) // ((1 << log2) - 1),
            )
            for log2 in range(max_log2, 0, -1)
        ),
        key=lambda candidate: (candidate.chunk_length * 2)
        + 2 * (2 ** math.ceil(math.log2(1 + candidate.gadget_calls)) - 1),
    )

    return best_opt.chunk_length
