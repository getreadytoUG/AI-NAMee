import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import json
import torch
import argparse
import numpy as np
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
 
def make_dataset(file_path):
    data_list = [] 
    meta_data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)
    
    print(len(raw_data))
    
    date_formats = [
        r"%Y년%m월%d일",
        r"%Y年%m月%d日",
        r"%Y.%m.%d",
        r"%Y/%m/%d"
    ]
    
    for data in raw_data:
        for date_format in date_formats:
            try:
                date = datetime.strptime(data['date'].split('(')[0], date_format)
                dt_to_str = date.strftime(r"%Y %m %d")
                date_list = dt_to_str.split(' ')
                date = {"year": date_list[0], "month": date_list[1], "day": date_list[2]}
                break
            except ValueError:
                continue  # 다음 날짜 형식으로 시도
        
        try:
            data_list.append(data['for_learn_summary'])
            meta_data.append({"filename": data['filename'], "original": data['original'], "year": date_list[0], "month": date_list[1], "day": date_list[2], 'committee_name': data['committee_name'], "meeting_number": data['meeting_number'], "agenda": data['agenda'], "law": data['law'], "questioner": f"{data['questioner_name']}", "questioner_position": f"{data['questioner_affiliation']}{data['questioner_position']}", "answerer": f"{data['answerer_name']}", "answerer_position": f"{data['answerer_affiliation']}{data['answerer_position']}"})
        except KeyError as e:
            print(data)
            print(e)
            
    return data_list, meta_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="파일 경로 입력")
    parser.add_argument("--data_path", required=True, help="파일 경로")
    args = parser.parse_args()
    data_path = args.data_path

    model_name = 'jhgan/ko-sroberta-multitask'
    embed_model = SentenceTransformerEmbeddings(model_name = model_name, model_kwargs = {'trust_remote_code': True})
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000000, chunk_overlap=0)
    
    data_list, meta_data = make_dataset(data_path)
    print(len(meta_data))
    print(len(data_list))
    doc_texts = text_splitter.create_documents(texts=data_list, metadatas=meta_data)
    
    # output_file_path = rf"../../data/faiss/{data_path.split('/')[-1].split('TL')[0].split('VL')[0]}"
    # output_file_path = rf"../../data/faiss/guk"
    # output_file_path = rf"../../data/faiss/bon"
    # output_file_path = rf"../../data/faiss/so"
    # output_file_path = rf"../../data/faiss/yeah"
    output_file_path = rf"../../data/faiss/teuk"
    
    if not os.path.isdir(output_file_path): 
        print(f"{output_file_path} 파일 생성중")
        doc_db = FAISS.from_documents(doc_texts, embed_model)
        doc_db.save_local(output_file_path)
        print('생성완료, ', len(doc_db.docstore._dict))
    else:
        print('이미 파일 존재')
        doc_db = FAISS.load_local(output_file_path, embed_model, allow_dangerous_deserialization=True)
        doc_db.add_documents(documents=doc_texts)
        doc_db.save_local(output_file_path)
        print(f'추가완료:, {len(doc_db.docstore._dict)}')