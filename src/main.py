from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from python.make_answer import legal_answer, minutes_answer

app = FastAPI()
app.mount("/static", StaticFiles(directory="js"), name="static")
templates = Jinja2Templates(directory="front")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 들어오는 질문에 대한 힌트
class Chat(BaseModel):
    data: str

# 법률 질문
@app.post("/legalchat")
async def make_legal_chat(question: Chat):
    print("## request complete ##")
    user_question = question.data

    print(f"user_question >> {user_question}")
    
    NAMee_answer = legal_answer(user_question)
    
    response = {
        "text": NAMee_answer,
    }
    print(f"response >> {response['text']}")
    return response


# 회의록 질문
@app.post("/minuteschat")
async def make_minutes_chat(question: Chat):
    print("## request complete ##")
    user_question = question.data

    print(f"user_question >> {user_question}")
    
    NAMee_answer = minutes_answer(user_question)
    
    response = {
        "text": NAMee_answer
    }
    
    print(f"response >> {response['text']}")
    return response

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/legal")
def read_legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})

@app.get("/minutes")
def read_minutes(request: Request):
    return templates.TemplateResponse("minutes.html", {"request": request})