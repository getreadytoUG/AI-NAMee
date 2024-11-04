from transformers import AutoModelForCausalLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import GenerationConfig
from peft import PeftModel

llama_model_path = "../model/Llama-3.2-3B-Instruct"
llama_model = AutoModelForCausalLM.from_pretrained(llama_model_path,device_map="cuda:0", attn_implementation="flash_attention_2", torch_dtype=torch.bfloat16)
llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_path, trust_remote_code=True)

lora_path = '../model/llama3.2_lora_model'
lora_model = PeftModel.from_pretrained(llama_model, lora_path)

llama_8b_model_path = "../model/Llama-3.1-8B-Instruct"
llama_8b_model = AutoModelForCausalLM.from_pretrained(llama_8b_model_path, device_map="cuda:0", attn_implementation="flash_attention_2",torch_dtype=torch.bfloat16)
llama_8b_tokenizer = AutoTokenizer.from_pretrained(llama_8b_model_path, trust_remote_code=True)

model_dic = {
    "Llama": llama_model,
    "LoRA": lora_model,
    "8B": llama_8b_model
}

tokenizer_dic = {
    "Llama": llama_tokenizer,
    "LoRA": llama_tokenizer,
    "8B": llama_8b_tokenizer
}

llm_legal_list = [{"role":"system", "content":"당신은 법률 기반 답변을 하는 LLM 모델입니다. 답변은 반드시 한국어로 하시고 존댓말을 사용해야 합니다."}]

llm_minutes_list = [{"role": "system", "content": "당신은 국회의 회의록 기반 답변을 하는 LLM 모델입니다. 답변은 반드시 한국어로 하시고 존댓말을 사용해야 합니다."}]

def answer_gen(x, chat_list, model_name, device):
    generation_config = GenerationConfig(
        temperature=0.8,
        top_p=0.8,
        top_k=100,
        max_new_tokens=1024,
        early_stopping=True,
        do_sample=True,
    )
    chat_list.append({'role':'user', 'content':x})
    
    use_model = model_dic[model_name]
    tokenizer = tokenizer_dic[model_name]

    q = tokenizer.apply_chat_template(chat_list, tokenize=True, return_tensors='pt', return_dict=True, add_generation_prompt=True)
    q = q.to(device)
    gened = use_model.generate(
        **q,
        generation_config=generation_config,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    result_str = tokenizer.decode(gened[0])

    start_tag = f"<|start_header_id|>assistant<|end_header_id|>\n\n"

    start_index = result_str.rfind(start_tag)
    if start_index != -1:
        result_str = result_str[start_index + len(start_tag):].strip()
    
    result_str = result_str.replace("<|eot_id|>", "")
    chat_list.append({'role':'assistant', 'content':result_str})
    return chat_list


def keyword_by_llm(question):
    chat_list = [{"role":"system", "content":"""당신은 사용자에게 도움을 주는 챗봇입니다.\n입력데이터에서 에서 년, 월, 일, 회의, 법률, 사람이름, 직책을 추출하여 딕셔너리 형태로 반환하세요. 출력은 아래와 같은 딕셔너리 형태입니다."""}]
    
    lora_made_result = answer_gen(question, chat_list, "LoRA", "cuda:0")[-1]["content"]
    
    try:
        keyword_dict = eval(lora_made_result)
    except:
        lora_made_result = answer_gen(question, chat_list, "LoRA", "cuda:0")[-1]
        keyword_dict = eval(lora_made_result)
        
    return keyword_dict


def llm_answer(question, subject):
    # llm_chat_list = answer_gen(question, llm_chat_list, "Llama", "cuda:0")
    # llm_chat_list = answer_gen(question, llm_chat_list, "Bllossom", "cuda:0")
    global llm_legal_list
    global llm_minutes_list
    
    if subject == "legal":
        llm_legal_list = answer_gen(question, llm_legal_list, "8B", "cuda:0")
        
        llm_made_answer = llm_legal_list[-1]["content"]
    else:
        llm_minutes_list = answer_gen(question, llm_minutes_list, "8B", "cuda:0")
        
        llm_made_answer = llm_minutes_list[-1]["content"]
        
    print(llm_made_answer)
    
    return llm_made_answer