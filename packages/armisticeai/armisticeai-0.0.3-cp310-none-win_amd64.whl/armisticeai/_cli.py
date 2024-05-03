import argparse


def valid_partition_percent(value):
    try:
        # Convert the comma-separated string to a list of floats
        parts = [float(num.strip()) for num in value.split(",")]
        if sum(parts) != 1.0:
            raise argparse.ArgumentTypeError("Percentages must sum to 1.")
        return parts
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Input should be a comma-separated list of numbers, like '0.3,0.5,0.2'"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Client participating in federated training."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="ArmisticeAI/OCTDL2024",
        help="The dataset to train on. Default is 'ArmisticeAI/OCTDL2024'. Can be local directory or HuggingFace dataset.",
    )
    parser.add_argument(
        "--checkpoint",
        "-c",
        type=str,
        default="google/vit-base-patch16-224-in21k",
        help="The model to start training from. Default is 'google/vit-base-patch16-224-in21k'.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="retinal_classifier/",
        help="Output directory to store training checkpoints. Default is 'retinal_classifier'.",
    )
    parser.add_argument(
        "--batch-size",
        "-b",
        type=int,
        default=16,
        help="The local batch size to be used during training. Default is 16.",
    )
    parser.add_argument(
        "--training",
        "-t",
        type=str,
        choices=["full", "lora_fp16", "lora_int8", "qlora_int4"],
        default="full",
        help="Training type. Default is 'full'.",
    )
    parser.add_argument(
        "--rank",
        "-r",
        type=int,
        default=64,
        help="Rank of LoRA matrix. Default is 64.",
    )
    parser.add_argument(
        "--alpha",
        "-a",
        type=int,
        default=128,
        help="Alpha of LoRA matrix. Default is 128 (alpha = 2*r is recommended).",
    )
    parser.add_argument(
        "--dap",
        action="store_true",
        help="If set, use DAP to perform secure aggregation. Default is false.",
    )
    parser.add_argument(
        "--dap-client-addr",
        "-d",
        type=str,
        default="localhost:9000",
        help="Address of DAP client to send parameters to. Default is 'localhost:9000'.",
    )
    # Adding arguments for test partitioning as optional
    parser.add_argument(
        "--test-partition",
        action="store_true",
        help="Enables artificially splitting the dataset for testing. If set, requires --partition-percent and --partition-index.",
    )
    parser.add_argument(
        "--partition-percent",
        "-p",
        type=valid_partition_percent,
        help="List of percentages (e.g., '0.3,0.5,0.2') that add up to 1, defining the dataset partition sizes. This partitioning is deterministic, aka the same elements will always end up in the same partition index for a given dataset and partition percents.",
    )
    parser.add_argument(
        "--partition-index",
        "-i",
        type=int,
        help="Index of the partition to use for testing (0-based, eg, 0, 1, or 2 if --split-percent is '0.3,0.5,0.2')",
    )
    args = parser.parse_args()

    # Check if test partitioning mode is enabled and if required arguments are provided
    if args.test_partition:
        if args.partition_percent is None or args.partition_index is None:
            parser.error(
                "--test-partition requires --partition-percent and --partition-index."
            )
