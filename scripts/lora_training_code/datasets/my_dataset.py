import os
import json
from sklearn.model_selection import train_test_split

def jload(path, mode="r"):
    with open(path, mode, encoding="utf-8") as f:
        json_data = []
        for line in f:
            json_data.append(json.loads(line))
    return json_data

def jload2(path, mode="r"):
    with open(path, mode, encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data


def get_preprocessed_llama(dataset_config, tokenizer, split):
    dataset = jload2(dataset_config.data_path)
    train_data, valid_data = train_test_split(dataset, test_size=2, random_state=dataset_config.seed)
    
    prompt = (f"<|start_header_id|>system<|end_header_id|>\n\n당신은 사용자에게 도움을 주는 챗봇입니다.\n입력데이터에서 에서 년, 월, 일, 회의, 법률, 사람이름, 직책을 모두 추출하여 딕셔너리 형태로 반환하세요. 출력은 딕셔너리 형태입니다.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{{data_instruction}}")
    output_prompt = (f"<|start_header_id|>assistant<|end_header_id|>\n\n{{data_output}}")
    
    def apply_prompt_template(sample):
        return {
            "input": prompt.format(data_instruction=sample['input']),
            "output": output_prompt.format(data_output=sample['output'])
        }
    

    def tokenize_add_label(sample):
        prompt = tokenizer.encode(tokenizer.bos_token + sample['input'] + tokenizer.eos_token, add_special_tokens=False)
        output = tokenizer.encode(sample['output'] + tokenizer.eos_token, add_special_tokens=False)
        
        sample = {
            "input_ids": prompt + output,
            "attention_mask": [1] * (len(prompt) + len(output)),
            "labels": [-100] * len(prompt) + output
        }
        return sample
    
    
    if split == "train":
        train_dataset = list(map(apply_prompt_template, train_data))
        train_dataset = list(map(tokenize_add_label, train_dataset))
        return train_dataset
    else:
        validation_dataset = list(map(apply_prompt_template, valid_data))
        validation_dataset = list(map(tokenize_add_label, validation_dataset))
        return validation_dataset