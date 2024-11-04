# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from functools import partial

from datasets.custom_dataset import get_custom_dataset,get_data_collator
from datasets.my_dataset import get_preprocessed_llama as get_llama_dataset 


DATASET_PREPROC = {
    "my_dataset": get_llama_dataset
}
DATALOADER_COLLATE_FUNC = {
    "custom_dataset": get_data_collator
}
