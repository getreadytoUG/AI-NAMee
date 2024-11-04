import os
import json
import openai
from datasets import load_dataset

# openai.api_key = OPENAI_API_KEY

folder_path_list = [
    r"../data/original/TL/TL_국정감사",
    r"../data/original/TL/TL_본회의",
    r"../data/original/TL/TL_소위원회",
    r"../data/original/TL/TL_예산결산특별위원회",
    r"../data/original/TL/TL_특별위원회",
    r"../data/original/VL/VL_국정감사",
    r"../data/original/VL/VL_본회의",
    r"../data/original/VL/VL_소위원회",
    r"../data/original/VL/VL_예산결산특별위원회",
    r"../data/original/VL/VL_특별위원회"
]

def add_summary_for_learn(dataset, summary):
    dataset["for_learn_summary"] = summary
    return dataset

def save_result(num):
    output_file_path_list = [
        r"../data/refine/국정감사TL.json",
        r"../data/refine/본회의TL.json",
        r"../data/refine/소위원회TL.json",
        r"../data/refine/예산결산특별위원회TL.json",
        r"../data/refine/특별위원회TL.json",
        r"../data/refine/국정감사VL.json",
        r"../data/refine/본회의VL.json",
        r"../data/refine/소위원회VL.json",
        r"../data/refine/예산결산특별위원회VL.json",
        r"../data/refine/특별위원회VL.json",
    ]
    output_file_path = output_file_path_list[num]
    all_data = []

    # 기존 파일 내용을 읽어옵니다.
    if os.path.exists(output_file_path):
        with open(output_file_path, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                print("Error decoding JSON from file, starting with an empty list.")
                all_data = []

    # 새로운 데이터를 기존 데이터에 추가합니다.
    all_data.extend(new_data)

    # 결과를 파일에 저장합니다.
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    with open(processed_files_path, "w", encoding="utf-8") as f:
        for file_name in task_end_list:
            f.write(f"{file_name}\n")

for i in range(10):
    folder_path = folder_path_list[i]
    file_names = os.listdir(folder_path)
    # 이미 처리된 파일 목록을 읽어옵니다.
    processed_files_path = r"../data/for_summary/task_end_list.txt"
    if os.path.exists(processed_files_path):
        with open(processed_files_path, "r", encoding="utf-8") as f:
            processed_files = set(f.read().splitlines())
    else:
        processed_files = set()

    task_end_list = list(processed_files)
    new_data = []

    for idx, file_name in enumerate(file_names):
        if file_name in processed_files:
            print(f"Skipping {file_name} as it is already processed.")
            continue
        
        file_path = os.path.join(folder_path, file_name)
        
        target_file = load_dataset("json", data_files=file_path)
        target_keyword = target_file["train"]["context"][0]

        print(file_name)
        if "for_learn_summary" not in target_file["train"].features:
            try: 
                target_result = openai.chat.completions.create(
                                        model="gpt-4o-mini",
                                        messages=[
                                            {"role": "system", "content": "당신은 LLM에 특허관련 지식을 강화시키기 위한 데이터셋 생성 작업을 수행하고 있습니다."},
                                            {"role": "user", "content": f"""
                                안녕하세요. 데이터셋 생성 작업을 수행하고 있습니다. 

                                주어진 회의 내용을 줄글 형태로 자세하게 20줄 내외로 정리해주세요.
                                회의 내용의 카테고리나 키워드가 같을 경우 줄바꿈 없이 하나의 문단으로 정리하면 됩니다.
                                글의 시작은 "이번 회의에서는" 으로 시작하면 되며 모든 문체는 "-다." 형식으로 유지해야 합니다.
                                당신은 주어진 회의 내용 안에서만 답변하세요. 이 외에 다른 문장은 응답하지 마세요. 당신의 응답을 바로 데이터셋으로 사용할 겁니다.

                                회의 내용:
                                {target_keyword}
                                """},
                                ],
                                )

                target_summary = target_result.choices[0].message.content
                target_file = target_file.map(add_summary_for_learn, fn_kwargs={"summary": target_summary})

                new_data.extend(target_file["train"])
                task_end_list.append(file_name)
        
            except Exception as e:
                print(f"OpenAI API error: {e}, {file_name}")
                
                break
            
        if idx % 1000 == 0:
            save_result(i)
            new_data = []
            print(f'{idx}번까지 저장 됨')    
        
        tmp = folder_path.split("/")
        print(f"{i} - {idx} 차례")
            
    save_result(i)