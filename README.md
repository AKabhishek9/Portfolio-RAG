# 🤖 Portfolio RAG: Intelligent Resume & Project Retrieval Engine

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.4%2B-green.svg)](https://python.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5%2B-orange.svg)](https://www.trychroma.com/)
[![Sentence-Transformers](https://img.shields.io/badge/Sentence--Transformers-all--MiniLM--L6--v2-yellow.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

A modular, entity-grounded **Retrieval-Augmented Generation (RAG)** pipeline that indexes and semantically retrieves factual data from **Abhishek Yadav's** professional credentials, full-stack projects, technical competencies, and academic background.

---

## 📌 Overview

Large Language Models frequently hallucinate or lack domain-specific, personal context. **Portfolio RAG** eliminates this by establishing an end-to-end semantic retrieval layer over a structured, verified markdown knowledge base extracted directly from Abhishek Yadav's professional resume.

### 🌟 Key Highlights
- **Explicit Entity Grounding**: Knowledge documents explicitly identify "Abhishek Yadav" across headers and paragraphs to prevent pronoun ambiguity after vector chunking.
- **Structured Metadata & YAML Frontmatter**: Every source document includes standardized headers (`id`, `title`, `entity`, `category`, `tags`, `summary`) ready for dense + metadata-filtered hybrid retrieval.
- **Dense Vector Embeddings**: Uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` generating 384-dimensional dense semantic vectors.
- **Persistent Vector Store**: Indexed with ChromaDB (`PersistentClient`), supporting dynamic upserts, metadata storage, and distance-to-similarity transformations.
- **Configurable Similarity Thresholding**: Filters out low-confidence context chunks using cosine similarity scoring before passing to the downstream LLM.
- **Pre-calibrated Query Benchmarks**: Documents include benchmark `Target RAG Retrieval Queries` to maximize semantic alignment during vector search.

---

## 🏗️ Architecture & Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Modular Knowledge Base                   │
│  (Resume, Projects, Skills, Experience, Education, etc.)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             LangChain Ingestion & Chunking                  │
│       DirectoryLoader & RecursiveCharacterTextSplitter      │
│            (Chunk Size: 800, Overlap: 150)                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Dense Embedding Generation                    │
│     SentenceTransformer ("all-MiniLM-L6-v2" - 384 dim)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Persistent Vector Database                  │
│                   ChromaDB Collection                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      RAGRetriever                           │
│       Cosine Similarity Ranking & Score Thresholding        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               LLM Context Injection & Generation            │
│            (Groq, OpenAI, Google Gemini, Ollama)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
Portfolio RAG/
├── .env.example                 # Template for environment variables & API tokens
├── .gitignore                   # Ignores .env, virtualenvs, cache, checkpoints
├── .python-version              # Python version pin (3.13)
├── pyproject.toml               # Project metadata and UV build specifications
├── requirements.txt             # Pip dependency definitions
├── uv.lock                      # Deterministic dependency lockfile
├── README.md                    # Project documentation
│
├── Notebook/
│   └── document.ipynb           # Interactive ingestion, embedding, and retrieval pipeline
│
├── knowledge/                   # Grounded, modular knowledge base
│   ├── README.md                # Knowledge base index & RAG manifest
│   ├── about.md                 # Profile, contact info, and executive summary
│   ├── achievements.md          # Hackathons & competitive programming milestones
│   ├── certifications.md        # Professional workshops & credentials (GFG, HCL GUVI, Azisly)
│   ├── education.md             # B.Tech degree, CGPA, coursework
│   ├── experience.md            # Work history, roles, and technical achievements
│   ├── profiles.md              # Social links (GitHub @AKabhishek9, LinkedIn, LeetCode)
│   ├── projects.md              # Overview and comparative project matrix
│   ├── resume.md                # Complete monolithic resume transcript
│   ├── skills.md                # Categorized technical competencies
│   ├── projects/
│   │   ├── arkface.md           # ArkFace: Real-time face recognition desktop app
│   │   ├── money-ledger.md      # Money Ledger: Offline-first finance PWA
│   │   └── quizai.md            # QuizAI: Adaptive AI quiz platform
│   └── vector_store/            # Persistent ChromaDB vector index and metadata
│
└── src/
    └── portfolio_rag/
        └── __init__.py          # Core package entry point
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.13+**
- Recommended: [uv](https://github.com/astral-sh/uv) (fast Python package manager) or standard `pip`

### 1. Clone the Repository
```bash
git clone https://github.com/AKabhishek9/Portfolio-RAG.git
cd Portfolio-RAG
```

### 2. Set Up Virtual Environment

**Using `uv` (Recommended):**
```bash
# Create virtual environment and sync dependencies
uv sync
```

**Using Standard `venv` & `pip`:**
```bash
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

A `.env.example` file is provided in the repository. Create your local `.env` file to configure optional API keys for Hugging Face (higher download limits) and your preferred LLM provider:

```bash
# Copy the example file to .env
cp .env.example .env
```

Edit `.env` with your preferred credentials:

```env
# Hugging Face token (prevents unauthenticated rate limit warnings for embeddings)
HF_TOKEN=your_huggingface_token_here

# LLM Providers (add key for whichever generator you want to integrate)
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# ChromaDB & Embedding settings
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=knowledge/vector_store
CHROMA_COLLECTION_NAME=portfolio_knowledge
```

> **Note:** `.env` is listed in `.gitignore` to prevent confidential keys from being pushed to GitHub.

---

## 🚀 Usage Guide

The complete RAG ingestion and retrieval workflow is implemented in [`Notebook/document.ipynb`](file:///Notebook/document.ipynb).

### 1. Ingestion & Text Splitting
Loads all markdown documents from `knowledge/` and chunks them into overlapping windows:
```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = DirectoryLoader("../knowledge", glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunks = text_splitter.split_documents(documents)
```

### 2. Generating Embeddings & Storing in ChromaDB
```python
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize embedding model (384 dimensions)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize persistent ChromaDB
client = chromadb.PersistentClient(path="../knowledge/vector_store")
collection = client.get_or_create_collection(name="portfolio_knowledge")
```

### 3. Querying with `RAGRetriever`
Query the vector store with custom `top_k` and similarity threshold filtering:
```python
# Query semantic retrieval
results = rag_retriever.retrieve(
    query="what are the skills abhishek have",
    top_k=5,
    score_threshold=0.0
)

for doc in results:
    print(f"Rank {doc['rank']} | Score: {doc['similarity_score']:.4f}")
    print(f"Source: {doc['metadata']['source']}")
    print(doc['content'])
    print("-" * 50)
```

---

## 🧠 Knowledge Base Coverage

| Category | Source File | Description |
| :--- | :--- | :--- |
| **Profile** | `knowledge/about.md` | Executive summary, core objectives, and contact details |
| **Skills** | `knowledge/skills.md` | Full-stack, ML/AI, languages, databases, DevOps tools |
| **Education** | `knowledge/education.md` | B.Tech in CSE, academic achievements, core CS coursework |
| **Experience** | `knowledge/experience.md` | Hands-on project work, engineering roles, and contributions |
| **Projects** | `knowledge/projects/*.md` | Deep dives into *Money Ledger*, *ArkFace*, and *QuizAI* |
| **Achievements** | `knowledge/achievements.md` | HackerRank Orchestrate (Rank 766/1,983), LeetCode solving |
| **Certificates** | `knowledge/certifications.md` | GeeksforGeeks, HCL GUVI AI Impact, Azisly AI simulation |
| **Profiles** | `knowledge/profiles.md` | GitHub, LinkedIn, LeetCode, and web portfolio handles |

---

## 🔌 Connecting Downstream LLMs (Next Step)

To generate human-like answers using retrieved context, you can connect an LLM (e.g., via Groq or LangChain):

```python
from langchain_core.prompts import ChatPromptTemplate
# Example with Groq (Fast & Free-tier friendly)
# from langchain_groq import ChatGroq

PROMPT_TEMPLATE = """
Answer the question based ONLY on the following verified context about Abhishek Yadav:

{context}

---
Question: {question}
Answer in a professional and concise manner:
"""

# Format retrieved documents as unified context
context_text = "\n\n".join([doc["content"] for doc in results])
prompt = PROMPT_TEMPLATE.format(context=context_text, question="What are Abhishek's key projects?")
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **RAG Framework:** LangChain (`langchain`, `langchain-community`, `langchain-core`)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/)
- **Embedding Model:** [Sentence-Transformers](https://sbert.net/) (`all-MiniLM-L6-v2`)
- **Document Parsers:** `pypdf`, `pymupdf`
- **Dependency Management:** [uv](https://github.com/astral-sh/uv) & standard `pip`

---

## 👤 Author & Contact

**Abhishek Yadav**
- **GitHub**: [@AKabhishek9](https://github.com/AKabhishek9)
- **Email**: [abhishek101242144@gmail.com](mailto:abhishek101242144@gmail.com)
- **Location**: Greater Noida, Uttar Pradesh, India

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
