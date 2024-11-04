# Fine-tuning with Single GPU  

- If use not Quantization  
`FSDP_CPU_RAM_EFFICIENT_LOADING=1 python finetuning.py  --use_peft --peft_method lora`  

- If use Quantization  
`FSDP_CPU_RAM_EFFICIENT_LOADING=1 python finetuning.py  --use_peft --peft_method lora --quantization 8bit`  

# Fine-tuning with Multi GPU  

- If use not Quantization with FSDP  
`torchrun --nnodes 1 --nproc_per_node 4  finetuning.py --enable_fsdp --use_peft --peft_method lora`  

- If use Quantization with FSDP  
` FSDP_CPU_RAM_EFFICIENT_LOADING=1 ACCELERATE_USE_FSDP=1 torchrun --nnodes 1 --nproc_per_node 4  finetuning.py --enable_fsdp  --quantization int4  --mixed_precision False --low_cpu_fsdp --use_peft --peft_method lora`  



