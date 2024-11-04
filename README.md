## 📚 AI-NAMee
#### 국회 회의록 기반 의정활동 및 대국민 알권리 보장 챗봇 서비스
#### 기간 : 2024-08-23 ~ 2024-10-28

----------------

## 🎁 기획
### "AI-NAMee : AI for National Assembly Meeting"
- "AI-NAMee"는 국회 회의록과 법률 문서를 분석하고, 이를 기반으로 사용자에게 정보를 전달해 주는 목적을 가진 챗봇 서비스입니다
- NER, RAG 기법, LoRA 사용 등을 이용하여 보다 정확한 답변을 이끌어 낼 수 있습니다.
- 국민의 관심사를 높히고 알 권리를 증진시키며 국회의 의정활동을 돕습니다.

<img width="100%" alt="image" src="https://github.com/user-attachments/assets/5f0ca80f-ac19-4356-88e4-424e7a0f7a7f">

<hr>

## 👨‍💻 My Role in Process
##### - 팀장, FAISS DB 생성, LoRA 학습 데이터 생성 및 학습, 모델 프롬프트 작성, PDF 작성

-------------------

## 🛍️ Dataset & Model
### 📚 Dataset
- [AI Hub "국회 회의록 기반 지식 검색 데이터"](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=71795)
- GPT-4o 를 활용하여 직접 작성한 데이터
  - RAG 수행을 위한 문서 데이터
  - LoRA 학습을 위한 데이터
- Namu Wiki 에서의 법률 용어 사전
  - Crawling 을 통하여 법과 관련된 내용 확인

<img width="100%" alt="image" src="https://github.com/user-attachments/assets/f51e0878-dc8b-4627-8568-adb0e9e9456a">

-------------------

### 💻 Model
- **meta/Llama-3.2-3B-Instruct**
- **meta/Llama-3.1-8B-Instruct**
- **jhgan/ko-sroberta-multitask**
- **fine tuned LoRA**-

<img width="100%" alt="image" src="https://github.com/user-attachments/assets/f9ba09e4-8506-424c-b0a5-4485982e2b21">
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/364b741e-d5d8-4f6d-9b02-e24ea363f0eb">

-------------------

## 🖥️ Front
- 챗봇이라는 컨셉에 걸맞게 사용하기 편한 인터페이스를 구성
- 회의록 기반 질문 시 답변의 근간이 되었던 pdf 링크를 함께 제공하여 신뢰성 확보

-------------------

##### 📦 최종 서비스 형태
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/9308bdbf-79b0-4491-8660-802607cdc5ab">
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/01a1ed7c-4f34-4105-bb07-191047724acc">
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/09259874-8006-4ed9-9af3-5b30002765fd">


---------------------------------------------------

### ⚙️ Skills & Tools

<p align="center">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/> 
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=PyTorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Meta-0467DF?style=flat-square&logo=Meta&logoColor=white"/>
  <img src="https://img.shields.io/badge/Hugging Face-FFD21E?style=flat-square&logo=Hugging Face&logoColor=white"/>
  <img src="https://img.shields.io/badge/Namu Wiki-008275?style=flat-square&logo=Namu Wiki&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=OpenAI&logoColor=white"/>
<!--   <img src="https://img.shields.io/badge/?style=flat-square&logo=&logoColor=white"/> -->
</p>
