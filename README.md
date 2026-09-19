#  Portfolio RAG

A simple RAG-based chatbot that can answer questions about **Abhishek Yadav's portfolio, skills, projects, education and experience**.

The main idea is simple:

> Store portfolio information → find the relevant information → give it to Gemini → generate an answer.

The backend is built with Python, LangChain, ChromaDB, Gemini Embedding 2, Gemini Flash and FastAPI. It is connected to the portfolio website through an API.

---

##  What This Project Does

This project works like a personal portfolio assistant.

A user can ask questions like:

- What skills does Abhishek have?
- What projects has he built?
- Tell me about QuizAI.
- What is Abhishek's education?
- What AI technologies does he know?

The chatbot first searches the portfolio knowledge base and then uses the relevant information to generate an answer.

This helps the chatbot answer from the actual portfolio data instead of making up random information.

---

##  How It Works (Architecture)

```text
                 Portfolio Website
                        |
                        | User asks a question
                        v
                  FastAPI Backend
                        |
                        v
                Gemini Embedding 2
                        |
                        v
                     ChromaDB
                        |
                  Relevant chunks
                        |
                        v
                  Gemini Flash
                        |
                        v
                   Final Answer
                        |
                        v
                  Portfolio Chatbot
```

---

##  Main Features

- Personal portfolio chatbot
- RAG-based question answering
- Markdown knowledge base
- Automatic document chunking
- Gemini Embedding 2 for embeddings
- 768-dimensional embeddings
- ChromaDB for vector storage
- Gemini Flash for answer generation
- FastAPI backend
- CORS support for the portfolio website
- Greeting responses without starting the full RAG system
- Local development support
- Render deployment support
- `/health` endpoint for health checking and waking the backend
- Knowledge base is rebuilt during deployment to avoid old/stale vectors

---

##  Knowledge Base

The `knowledge/` folder contains the information used by the chatbot.

It includes information about:

- About Abhishek
- Skills
- Education
- Experience
- Projects
- Achievements
- Certifications
- Online profiles

Example:

```text
knowledge/
├── about.md
├── achievements.md
├── certifications.md
├── education.md
├── experience.md
├── profiles.md
├── projects.md
├── resume.md
├── skills.md
└── projects/
    ├── arkface.md
    ├── money-ledger.md
    └── quizai.md
```

---

## 📂 Project Structure

```text
Portfolio RAG/
│
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── README.md
│
├── knowledge/
│   ├── about.md
│   ├── achievements.md
│   ├── certifications.md
│   ├── education.md
│   ├── experience.md
│   ├── profiles.md
│   ├── projects.md
│   ├── resume.md
│   ├── skills.md
│   ├── projects/
│   │   ├── arkface.md
│   │   ├── money-ledger.md
│   │   └── quizai.md
│   └── vector_store/
│
└── src/
    └── portfolio_rag/
        ├── __init__.py
        ├── api.py
        ├── ingest.py
        └── rag.py
```

---

##  Technologies Used

| Technology | Use |
|---|---|
| Python 3.13+ | Main programming language |
| LangChain | RAG and LLM integration |
| Gemini Embedding 2 | Creates document and query embeddings |
| Gemini Flash | Generates final answers |
| ChromaDB | Stores and searches embeddings |
| FastAPI | Backend API |
| uv | Python package management |
| Render | Backend deployment |

---

##  Environment Variables

Create a `.env` file in the project root:

```env
API_KEY="your_gemini_api_key"
API_MODEL="gemini-3.6-flash"
```

Never upload the real `.env` file to GitHub.

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/AKabhishek9/Portfolio-RAG.git
cd Portfolio-RAG
```

### 2. Install dependencies

Using `uv`:

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create `.env`:

```env
API_KEY="your_gemini_api_key"
API_MODEL="gemini-3.6-flash"
```

---

##  Build the Knowledge Base

The ingestion script loads the Markdown files from `knowledge/`, splits them into chunks and creates embeddings.

Current chunk settings:

```text
Chunk size    : 800
Chunk overlap : 150
```

Run:

```bash
PYTHONPATH=src python -m portfolio_rag.ingest
```

The script:

1. Loads the Markdown files.
2. Splits them into chunks.
3. Creates Gemini embeddings.
4. Resets the old ChromaDB collection.
5. Adds the new documents and embeddings.

Resetting the collection helps prevent old information from staying in the vector database after knowledge files are changed.

---

##  Running the API Locally

Start FastAPI with:

```bash
PYTHONPATH=src uvicorn portfolio_rag.api:app --reload
```

The API normally runs at:

```text
http://127.0.0.1:8000
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### Home

```text
GET /
```

Returns the API status.

### Health Check

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

The portfolio calls this endpoint when the website opens. This gives the Render backend a chance to wake up before the user starts using the chatbot.

### Chat

```text
POST /chat
```

Request:

```json
{
  "question": "What skills does Abhishek have?"
}
```

Response:

```json
{
  "answer": "..."
}
```

---

##  Portfolio Connection

The chatbot frontend sends questions to the deployed FastAPI backend.

Portfolio:

```text
https://myportfolio-2dc17.web.app/
```

RAG API:

```text
https://portfolio-rag-rayf.onrender.com
```

When the portfolio opens, it sends a request to:

```text
https://portfolio-rag-rayf.onrender.com/health
```

This helps start the Render service before the user sends a chatbot question.

The portfolio itself does not wait for this request, so the website can continue loading normally.

---

##  Render Deployment

The backend is deployed on Render.

### Build Command

```bash
pip install -r requirements.txt && PYTHONPATH=src python -m portfolio_rag.ingest
```

### Start Command

```bash
PYTHONPATH=src uvicorn portfolio_rag.api:app --host 0.0.0.0 --port $PORT
```

Render environment variables:

```env
API_KEY=your_gemini_api_key
API_MODEL=gemini-3.6-flash
```

The Render Free service can sleep when there is no traffic. Because of this, the portfolio sends a `/health` request when someone opens the website.

The first request after the service has been sleeping can still take some time because the server needs to start.

---

##  RAG Process

The main RAG process is:

```text
1. User asks a question
        ↓
2. Question is converted into an embedding
        ↓
3. ChromaDB searches for similar knowledge
        ↓
4. Relevant documents are retrieved
        ↓
5. Retrieved content is added to the prompt
        ↓
6. Gemini Flash generates the answer
        ↓
7. Answer is returned to the portfolio
```

The chatbot is instructed to use only the retrieved portfolio information.

---

##  Keeping Answers Grounded

The prompt tells Gemini to:

- Use only the provided portfolio context.
- Not invent skills or projects.
- Not assume missing information.
- Answer in third person.
- Keep answers concise and professional.
- Not expose internal RAG details.

This makes the chatbot more suitable for an HR-style portfolio assistant.

---

##  Example Questions

```text
What skills does Abhishek have?

What projects has Abhishek built?

Tell me about QuizAI.

Tell me about Money Ledger.

What is Abhishek's education?

What AI technologies does he know?

What certifications does he have?
```

---

##  Current Embedding Setup

```text
Embedding Model : gemini-embedding-2
Dimensions      : 768
Vector Database : ChromaDB
Distance        : Cosine
```

The old Sentence Transformers embedding setup is no longer used.

---

##  Author

**Abhishek Yadav**

- GitHub: https://github.com/AKabhishek9
- Portfolio: https://myportfolio-2dc17.web.app/

---

##  License

This project is licensed under the MIT License.

---

##  Final Note

I built this project to understand how RAG works in a real project.

I started with a local RAG system and then connected it with a FastAPI backend and my portfolio website.

The main goal is to make my portfolio interactive so an HR or recruiter can directly ask questions about my skills, projects, education and experience.
