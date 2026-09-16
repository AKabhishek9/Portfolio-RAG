from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from portfolio_rag.rag import EmbeddingManager, VectorStore


BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
VECTOR_STORE_DIR = KNOWLEDGE_DIR / "vector_store"


def main():
    print("Loading knowledge base...")

    loader = DirectoryLoader(
        str(KNOWLEDGE_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    texts = [chunk.page_content for chunk in chunks]

    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.generate_embeddings(texts)

    vector_store = VectorStore(
        persist_directory=str(VECTOR_STORE_DIR)
    )

    vector_store.add_documents(
        chunks,
        embeddings
    )

    print("Knowledge ingestion completed successfully.")


if __name__ == "__main__":
    main()