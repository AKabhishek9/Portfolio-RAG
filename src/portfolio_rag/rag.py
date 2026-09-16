from pathlib import Path
from typing import List, Dict, Any

import os
import numpy as np
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# Environment
# ============================================================

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found in .env")


# ============================================================
# File Ingestion
# ============================================================

def load_file(file_path):
    """
    Load a file using the appropriate loader based on its extension.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in [".md", ".txt"]:
        loader = TextLoader(
            str(path),
            encoding="utf-8"
        )

    elif extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))

    elif extension == ".csv":
        loader = CSVLoader(str(path))

    elif extension == ".pptx":
        loader = UnstructuredPowerPointLoader(str(path))

    elif extension in [".xlsx", ".xls"]:
        loader = UnstructuredExcelLoader(str(path))

    else:
        print(f"Skipping unsupported file: {path}")
        return []

    try:
        return loader.load()

    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return []


def load_knowledge_base(directory="../knowledge"):
    """
    Load all supported files recursively from the knowledge directory.
    """

    documents = []

    knowledge_path = Path(directory)

    supported_extensions = {
        ".md",
        ".txt",
        ".pdf",
        ".docx",
        ".csv",
        ".pptx",
        ".xlsx",
        ".xls",
    }

    for file_path in knowledge_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        print(f"Loading: {file_path}")

        file_documents = load_file(file_path)

        documents.extend(file_documents)

    return documents


# ============================================================
# Embedding Manager
# ============================================================

class EmbeddingManager:
    """
    Handles document embedding generation
    using Sentence Transformer.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model = None

        self._load_model()

    def _load_model(self):

        print(
            f"Loading embedding model: "
            f"{self.model_name}"
        )

        self.model = SentenceTransformer(
            self.model_name
        )

        print(
            "Embedding model loaded successfully. "
            f"Dimensions: "
            f"{self.model.get_embedding_dimension()}"
        )

    def generate_embeddings(
        self,
        texts: List[str]
    ) -> np.ndarray:

        if not self.model:
            raise ValueError(
                "Model not loaded"
            )

        print(
            f"Generating embeddings for "
            f"{len(texts)} texts..."
        )

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        print(
            f"Generated embeddings with shape: "
            f"{embeddings.shape}"
        )

        return embeddings


# ============================================================
# Vector Store
# ============================================================

class VectorStore:
    """
    Manages document embeddings in ChromaDB.
    """

    def __init__(
        self,
        collection_name: str = "portfolio_knowledge",
        persist_directory: str = "../knowledge/vector_store"
    ):

        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.client = None
        self.collection = None

        self._initialize_store()

    def _initialize_store(self):

        os.makedirs(
            self.persist_directory,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "description":
                        "Portfolio knowledge embeddings for RAG",
                    "hnsw:space": "cosine"
                }
            )
        )

        print(
            f"Vector store initialized. "
            f"Collection: {self.collection_name}"
        )

        print(
            f"Existing documents in collection: "
            f"{self.collection.count()}"
        )

    def add_documents(
        self,
        documents: List[Any],
        embeddings: np.ndarray
    ):

        if len(documents) != len(embeddings):

            raise ValueError(
                "Number of documents must match "
                "number of embeddings"
            )

        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i, (
            doc,
            embedding
        ) in enumerate(
            zip(documents, embeddings)
        ):

            source = doc.metadata.get(
                "source",
                "unknown"
            )

            doc_id = (
                f"{source}_{i}"
                .replace("\\", "_")
                .replace("/", "_")
            )

            ids.append(doc_id)

            metadata = dict(
                doc.metadata
            )

            metadata["doc_index"] = i
            metadata["content_length"] = (
                len(doc.page_content)
            )

            metadatas.append(metadata)

            documents_text.append(
                doc.page_content
            )

            embeddings_list.append(
                embedding.tolist()
            )

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas,
            documents=documents_text
        )

        print(
            f"Successfully added/updated "
            f"{len(documents)} documents"
        )

        print(
            f"Total documents in collection: "
            f"{self.collection.count()}"
        )


# ============================================================
# RAG Retriever
# ============================================================

class RAGRetriever:
    """
    Handles query-based retrieval
    from the vector store.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_manager: EmbeddingManager
    ):

        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:

        print(
            f"Retrieving documents for query: "
            f"'{query}'"
        )

        query_embedding = (
            self.embedding_manager
            .generate_embeddings([query])[0]
        )

        results = (
            self.vector_store
            .collection
            .query(
                query_embeddings=[
                    query_embedding.tolist()
                ],
                n_results=top_k
            )
        )

        retrieved_docs = []

        if (
            results["documents"]
            and results["documents"][0]
        ):

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            ids = results["ids"][0]

            for i, (
                doc_id,
                document,
                metadata,
                distance
            ) in enumerate(
                zip(
                    ids,
                    documents,
                    metadatas,
                    distances
                )
            ):

                similarity_score = 1 - distance

                if (
                    similarity_score
                    >= score_threshold
                ):

                    retrieved_docs.append({
                        "id": doc_id,
                        "content": document,
                        "metadata": metadata,
                        "similarity_score":
                            similarity_score,
                        "distance": distance,
                        "rank": i + 1
                    })

        print(
            f"Retrieved "
            f"{len(retrieved_docs)} "
            f"documents"
        )

        return retrieved_docs


# ============================================================
# Initialize RAG Components
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = (
    BASE_DIR / "knowledge"
)

VECTOR_STORE_DIR = (
    KNOWLEDGE_DIR / "vector_store"
)


embedding_manager = EmbeddingManager()

vectorstore = VectorStore(
    persist_directory=str(
        VECTOR_STORE_DIR
    )
)

rag_retriever = RAGRetriever(
    vectorstore,
    embedding_manager
)


# ============================================================
# Gemini
# ============================================================

llm = ChatGoogleGenerativeAI(
    api_key=API_KEY,
    model="gemini-3.6-flash",
    max_tokens=1024
)


# ============================================================
# RAG Function
# ============================================================

def rag_simple(
    query: str,
    top_k: int = 5
):

    results = rag_retriever.retrieve(
        query,
        top_k=top_k
    )

    context = (
        "\n\n".join(
            [
                doc["content"]
                for doc in results
            ]
        )
        if results
        else "No relevant documents found."
    )

    prompt = f"""
Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "\n".join(
            block["text"]
            for block in response.content
            if block.get("type") == "text"
        )

    return answer