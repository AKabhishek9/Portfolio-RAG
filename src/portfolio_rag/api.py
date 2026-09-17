from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="Portfolio RAG",
    version="1.0.0"
)


# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://myportfolio-2dc17.web.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# Request Model
# ------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Portfolio RAG API"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question."
        }

    from portfolio_rag.rag import rag_simple
    answer = rag_simple(question)

    return {
        "answer": answer
    }