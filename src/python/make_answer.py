import requests
from bs4 import BeautifulSoup as BS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import warnings
from python.model_use import keyword_by_llm, llm_answer
warnings.filterwarnings(action="ignore")

docs_embeddings = SentenceTransformerEmbeddings(model_name='jhgan/ko-sroberta-multitask', model_kwargs={'trust_remote_code': True})


# 크롤링 하는 함수
def crawling(keyword):
    url = f"http://www.namu.wiki/w/{keyword}"
    
    response = requests.get(url)
    
    # 크롤링 성공
    if response.status_code == 200:
        soup = BS(response.content, "html.parser")
    
        divs_with_word = soup.find_all('div', class_="wiki-heading-content")
        
        result_docs = divs_with_word[0].text + "\n" + divs_with_word[1].text + "\n" + divs_with_word[2].text
        
        print(result_docs)
        
        return result_docs
        
    else:
        print("크롤링 실패, 에러 발생")
        
        return None


# 법률 기반 질문에 대한 응답을 만들어 내는 함수
def legal_answer(question):
    legal = keyword_by_llm(question)["법률"]
    
    legal_paper = crawling(legal)
    
    input_question = f"""
    다음 문서를 참고하여 질문에 한글로 답해주세요.
    문서:
    {legal_paper}
    질문:
    {question}
    """
    
    NAMee_answer = llm_answer(input_question, "legal")
    
    print(NAMee_answer)
        
    return NAMee_answer
    


# 회의록 기반 질문에 대한 응답을 만들어 내는 함수
def minutes_answer(question):
    keyword_dict = keyword_by_llm(question)
    
    print(keyword_dict)
    
    year = keyword_dict["년"]
    month = keyword_dict["월"]
    day = keyword_dict["일"]
    committee_name = keyword_dict["회의"]
    name = keyword_dict["이름"]
    position = keyword_dict["직책"]
    
    keyword_list = [year, month, day, name, position]
    
    key_list = ["year", "month", "day", "name", "position"]
    
    ner_filter = {}
    
    del_list = []
    
    for i in range(len(keyword_list)):
        if keyword_list[i]:
            try:
                ner_filter[key_list[i]] = str(keyword_list[i]).replace(" ", "")
                del_list.append(str(keyword_list[i]).replace(" ", ""))
            except:
                pass

    print("committee_name: " ,committee_name)
    
    if committee_name : 
        try:
            encoding_dict = {
                "국정감사": "guk",
                "본회의": "bon",
                "소위원회": "so",
                "예산결산특별위원회": "yeah",
                "특별위원회": "teuk"
            }

            encoded_meeting = encoding_dict[committee_name]            
            print(ner_filter)
            doc_db = FAISS.load_local(rf"../data/faiss/{encoded_meeting}", docs_embeddings, allow_dangerous_deserialization=True)
            if keyword_dict['법률']:
                result = doc_db.similarity_search_with_relevance_scores(question, k=200, filter=ner_filter)
                print(result)
            else:
                # None이 아닌 값들만 필터링
                # 조건에 맞는 page_content 찾기
                result = []

                for document in doc_db.docstore._dict.values():
                    metadata = document.metadata  # Document 객체에서 metadata 접근
                    if all(metadata.get(k) == v for k, v in ner_filter.items()):
                        result.append([document])  # Document 객체에서 page_content 접근

            print(result)
            if result:
                original_list = []

                for r in result:
                    original_list.append([r[0].metadata["filename"], r[0].metadata["original"]])
                    if(len(original_list) == 5):
                        break
                    
                result_doc = ""

                for i in range(len(result)):
                    tmp = result[i]

                    result_doc += str(tmp)


                question_word_list = question.split(" ")
                filtered_question_word_list = []

                for word in question_word_list:
                    if not any(del_word in word for del_word in del_list):
                        filtered_question_word_list.append(word)

                last_question = " ".join(filtered_question_word_list) + " "
                print(last_question)

                print(result_doc)
                input_question = f"""
                다음 문서를 참고하여 질문에 한글로 답해주세요.
                문서:
                {result_doc}
                질문:
                {last_question}
                반드시 질문의 내용에 대답하십시오. 문서는 단순 참고용입니다.
                """

                # input_question 을 LLM 에 넣어 답변 추출 후 반환
                NAMee_answer = llm_answer(input_question, "minutes")

                if original_list:
                    NAMee_answer += f" \\n 회의록 원문은 다음을 참고해 주세요. \\n "

                    for i in original_list:
                        NAMee_answer += "pdf file : "+ "<a href=" + i[1] + ">" + i[0] + "</a>" + " \\n "

                print("NAMee_answer:", NAMee_answer)
            else:
                NAMee_answer = "질문자의 질문과 연관된 문서를 찾지 못했어요. \\n 다시 한번 확인해 주시겠어요?"  
        except:
            NAMee_answer = "질문자의 질문과 연관된 문서를 찾지 못했어요. \\n 다시 한번 확인해 주시겠어요?"
    else:
        NAMee_answer = "질문자의 질문과 연관된 문서를 찾지 못했어요. \\n 다시 한번 확인해 주시겠어요?"
        
    return NAMee_answer
    
