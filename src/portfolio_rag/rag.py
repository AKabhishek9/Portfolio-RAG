import os
from pathlib import Path

import chromadb
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ENVIRONMENT

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_MODEL = os.getenv("API_MODEL", "gemini-3.6-flash")

if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")


# EMBEDDING MANAGER

class EmbeddingManager:
    """
    Generates embeddings using Google's Gemini Embedding 2 model.
    """

    def __init__(
        self,
        model_name="gemini-embedding-2",
        output_dimensionality=768,
        batch_size=20,
    ):
        from google import genai
        from google.genai import types

        self.model_name = model_name
        self.output_dimensionality = output_dimensionality
        self.batch_size = batch_size

        self.genai = genai
        self.types = types

        self.client = genai.Client(api_key=API_KEY)

    def generate_embeddings(self, texts, is_query=False):
        """
        Generate embeddings for a list of texts.

        is_query=False -> document embeddings
        is_query=True  -> query embedding
        """

        if not texts:
            return np.empty(
                (0, self.output_dimensionality),
                dtype=np.float32,
            )

        if is_query:
            prefix = (
                "Find portfolio information relevant to this question:\n"
            )
        else:
            prefix = (
                "Retrieve relevant portfolio information from this document:\n"
            )

        all_embeddings = []

        # Process texts in batches
        for start in range(0, len(texts), self.batch_size):

            batch = texts[start:start + self.batch_size]

            contents = [
                self.types.Content(
                    parts=[
                        self.types.Part.from_text(
                            text=f"{prefix}{text}"
                        )
                    ]
                )
                for text in batch
            ]

            result = self.client.models.embed_content(
                model=self.model_name,
                contents=contents,
                config=self.types.EmbedContentConfig(
                    output_dimensionality=self.output_dimensionality
                ),
            )

            all_embeddings.extend(
                embedding.values
                for embedding in result.embeddings
            )

        embeddings = np.asarray(
            all_embeddings,
            dtype=np.float32,
        )

        if len(embeddings) != len(texts):
            raise ValueError(
                f"Expected {len(texts)} embeddings, "
                f"but received {len(embeddings)}."
            )

        print(f"Generated embeddings: {embeddings.shape}")

        return embeddings


# VECTOR STORE

class VectorStore:
    """
    ChromaDB vector store.
    """

    def __init__(
        self,
        persist_directory: str,
        collection_name: str = "portfolio_knowledge",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine"
            },
        )

    def reset_collection(self):
        """Delete and recreate the current Chroma collection."""

        try:
            self.client.delete_collection(
                name=self.collection_name
            )
            print(f"Deleted old collection: {self.collection_name}")
        except Exception:
            pass

        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={
                "hnsw:space": "cosine"
            },
        )

        print(f"Created fresh collection: {self.collection_name}")

    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to ChromaDB.
        """

        if not documents:
            return

        ids = []
        texts = []
        metadatas = []
        vectors = []

        for index, (document, embedding) in enumerate(
            zip(documents, embeddings)
        ):
            ids.append(
                f"{document.metadata.get('source', 'unknown')}_{index}"
            )

            texts.append(document.page_content)

            metadatas.append(
                document.metadata
            )

            vectors.append(
                embedding.tolist()
            )

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=vectors,
        )

        print(
            f"Added {len(documents)} documents "
            f"to collection '{self.collection_name}'"
        )

    def search(
        self,
        query_embedding,
        top_k=5,
    ):
        """
        Search the vector store using cosine similarity.
        """

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
        )

        return results


# RAG RETRIEVER

class RAGRetriever:
    """
    Retrieves relevant portfolio knowledge from ChromaDB.
    """

    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vector_store: VectorStore,
    ):
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k=5,
    ):
        """
        Convert the user query into an embedding
        and retrieve the most relevant documents.
        """

        query_embedding = self.embedding_manager.generate_embeddings(
            [query],
            is_query=True,
        )[0]

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        retrieved_documents = []

        for document, distance, metadata in zip(
            documents,
            distances,
            metadatas,
        ):
            retrieved_documents.append(
                {
                    "content": document,
                    "distance": distance,
                    "metadata": metadata,
                }
            )

        return retrieved_documents


# PATHS

BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = BASE_DIR / "knowledge"

VECTOR_STORE_DIR = KNOWLEDGE_DIR / "vector_store"


# LAZY RAG INITIALIZATION

embedding_manager = None
vectorstore = None
rag_retriever = None
llm = None


def initialize_rag():
    """
    Initialize RAG components only when needed.

    This keeps API startup lightweight.
    """

    global embedding_manager
    global vectorstore
    global rag_retriever
    global llm

    if (
        embedding_manager is not None
        and vectorstore is not None
        and rag_retriever is not None
        and llm is not None
    ):
        return

    print("Initializing RAG...")

    # Gemini Embedding 2
    embedding_manager = EmbeddingManager()

    # ChromaDB
    vectorstore = VectorStore(
        persist_directory=str(VECTOR_STORE_DIR)
    )

    # Retriever
    rag_retriever = RAGRetriever(
        embedding_manager=embedding_manager,
        vector_store=vectorstore,
    )

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
    model=API_MODEL,
    google_api_key=API_KEY,
    temperature=0.2,
    max_output_tokens=300,
    )

    print("RAG initialized successfully.")


# RAG FUNCTION

def rag_simple(
    question: str,
    top_k=5,
):

    question = question.strip()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if question.lower() in greetings:
        return (
            "Hi! I'm Abhishek's portfolio assistant. "
            "Feel free to ask about his projects, skills, education, "
            "or experience."
        )


    initialize_rag()

    # Retrieve relevant documents

    retrieved_documents = rag_retriever.retrieve(
        question,
        top_k=top_k,
    )

    if not retrieved_documents:
        return (
            "I don't have enough information in my portfolio "
            "knowledge base to answer that."
        )

    # Build context

    context_parts = []

    for item in retrieved_documents:
        context_parts.append(
            item["content"]
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    # Prompt

    prompt = f"""
            You are an HR-style assistant for Abhishek Yadav's portfolio.

            Answer the user's question using ONLY the information in the context.

            Rules:
            - Give a complete answer.
            - Never stop in the middle of a sentence or list.
            - If listing items, include ALL relevant items available in the context.
            - Do not create empty bullet points.
            - Do not invent information.
            - Do not assume information that is not in the context.
            - If the context does not contain the answer, say:
            "This information is not available in Abhishek's portfolio."
            - Keep the answer concise and professional.
            - Answer in third person.
            - Do not mention RAG, embeddings, vector databases, ChromaDB,
            prompts, or internal system details.
            - Do not provide personal contact information unless specifically asked.

            Context:
            {context}

            User Question:
            {question}

            Answer:
        """
    
    # Generate answer

    response = llm.invoke(prompt)

    answer = response.content

    # Convert Gemini structured response to plain text
    if isinstance(answer, str):
        return answer.strip()

    if isinstance(answer, list):
        text_parts = []

        for item in answer:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    text_parts.append(text)

            elif hasattr(item, "text"):
                text = item.text
                if text:
                    text_parts.append(text)

        if text_parts:
            return "\n".join(text_parts)

    return str(answer)