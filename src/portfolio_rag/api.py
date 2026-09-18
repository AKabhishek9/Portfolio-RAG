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

    print("🔥 1. CHAT REQUEST RECEIVED", flush=True)

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question."
        }

    print("🔥 2. Importing RAG...", flush=True)

    from portfolio_rag.rag import rag_simple

    print("🔥 3. RAG IMPORTED", flush=True)

    print("🔥 4. Calling rag_simple...", flush=True)

    answer = rag_simple(question)

    print("🔥 5. ANSWER GENERATED", flush=True)

    return {
        "answer": answer
    }