from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import fetch_topics, fetch_quizzes_by_topic, fetch_questions_by_quiz_id
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(
    title="Quiz App API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(RequestValidationError) 

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()} 

    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(

        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error" } 

    )


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/topics")
async def get_topics():
    topics = fetch_topics()
    return topics

@app.get("/topics/{topic_id}/quizzes")
async def get_quizzes_by_topic(topic_id: str):
    quizzes = await fetch_quizzes_by_topic(topic_id)
    if "error" in quizzes:
        return {"message": quizzes["error"]}
    return quizzes

@app.get("/topics/{topic_id}/quizzes/{quiz_id}/questions")
async def get_questions_by_quiz_id(topic_id: str, quiz_id: str):
    questions = await fetch_questions_by_quiz_id(topic_id, quiz_id)
    return questions