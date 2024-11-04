# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime

run_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S") 

@dataclass
class wandb_config:
    project: str = 'finetuning_sroberta' # wandb project name
    entity: Optional[str] = None # wandb entity name
    job_type: Optional[str] = None
    tags: Optional[List[str]] = None
    group: Optional[str] = None
    notes: Optional[str] = None
    mode: Optional[str] = None
    name: Optional[str] = run_time + "(llama 3.2 3B)"