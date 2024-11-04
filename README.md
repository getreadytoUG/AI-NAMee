# AI-NAMee

## 본 설명서는 Visual Studio 에서 실행할 때의 코드입니다.

### 1. 백그라운드 설정
1. conda 가상환경 설치
- conda create -n namee python=3.10.14
- conda activate namee 
- cd scripts
- conda env export > environment.yaml

2. pip 모듈 설치
- 현재 위치가 scripts 일 때 (아니라면 cd scripts)
- pip install -r requirements.txt


### 2. 서버 실행 및 프론트 단 실행

1. 파이썬 서버 실행
- 콘솔창을 하나 열어서 cd src 명령어를 사용해 src 폴더로 이동
- [uvicorn main:app] 으로 파이썬 서버 실행

3. 프론트 실행
- uvicorn main:app 을 실행할 때 터미널 창에 출력되는 주소를 [ctrl + 클릭] 하여 들어가거나, [127.0.0.1:8000](http://127.0.0.1:8000) 에 접속하여 확인
- 각 task 별 페이지에 접속하여 질문 입력


### 3. 데이터 정제
1. refine 데이터
- 원본 데이터를 정제한 데이터로 for_summary 라는 카테고리를 하나 더 만들어 이 부분을 RAG 를 위한 문서로 작성
- 회의록 기반 질문이 들어오면 먼저 유사도가 가장 높은 문서를 추출
- 할루시네이션 방지를 위해 수행
- faiss DB 사용
    - Facebook 에서 만든 DB 형태로 유사도 계산에 강점이 있어서 사용
    - 이후 metadata 를 활용하여 filter 까지 하여 사용자가 원하는 조건의 문서 내에서만 검색되도록 함

2. LoRA 데이터 생성
- GPT API를 사용하여 여러 예상 질문들과 그에 대한 답변을 생성하게 하여 질문에서 필요한 부분을 추출하는 동작을 수행하는 LoRA 모델을 학습
- data 폴더 안 target_summary.json 을 사용