# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from dataclasses import dataclass


@dataclass
class train_config:
    # model_name: str="/media/user/datadisk/LLM_models/Llama-3.2-3B-Instruct"
    model_name: str="/media/user/datadisk/LLM_models/llama-3.2-Korean-Bllossom-3B"
    tokenizer_name: str=None
    enable_fsdp: bool=False # shards model parameters, optimizer states and gradients across DDP ranks
    low_cpu_fsdp: bool=False # saves cpu memory by loading pretrained model on rank0 only
    run_validation: bool=True
    batch_size_training: int=2
    batching_strategy: str="padding" #alternative: padding
    context_length: int=2048
    gradient_accumulation_steps: int=128
    gradient_clipping: bool = True
    gradient_clipping_threshold: float = 1.0
    num_epochs: int=30
    max_train_step: int=0
    max_eval_step: int=0
    num_workers_dataloader: int=10
    lr: float=2e-4
    weight_decay: float=0.0
    gamma: float= 0.85 # multiplicatively decay the learning rate by gamma after each epoch
    seed: int=42
    use_fp16: bool=False
    mixed_precision: bool=True
    val_batch_size: int=2
    dataset = "my_dataset"
    peft_method: str = "lora" # None, llama_adapter (Caution: llama_adapter is currently not supported with FSDP)
    use_peft: bool=False # use parameter efficient fine tuning
    from_peft_checkpoint: str="" # if not empty and use_peft=True, will load the peft checkpoint and resume the fine-tuning on that checkpoint
    output_dir: str = "/home/user/eomjimin/AI_Namee/Fine-tuning/lora_output"
    freeze_layers: bool = False
    num_freeze_layers: int = 1
    quantization: str = None
    one_gpu: bool = False
    save_model: bool = True
    dist_checkpoint_root_folder: str="./output/llama3.2-SFT-lora7/FSDP" # will be used if using FSDP
    dist_checkpoint_folder: str="fine-tuned" # will be used if using FSDP
    save_optimizer: bool=False # will be used if using FSDP
    use_fast_kernels: bool = False # Enable using SDPA from PyTroch Accelerated Transformers, make use Flash Attention and Xformer memory-efficient kernels
    use_wandb: bool = True # Enable wandb for experient tracking
    save_metrics: bool = False # saves training metrics to a json file for later p                                                      otting
    flop_counter: bool = False # Enable flop counter to measure model throughput, can not be used with pytorch profiler at the same time.
    flop_counter_start: int = 3 # The step to start profiling, default is 3, which means after 3 steps of warmup stage, the profiler will start to count flops.
    use_profiler: bool = False # Enable pytorch profiler, can not be used with flop counter at the same time.
    profiler_dir: str = "PATH/to/save/profiler/results" # will be used if using profiler
