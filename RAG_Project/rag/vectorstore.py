import os
import shutil

CHROMA_DIR = "./chroma_db"
COLLECTION  = "rag_documents"
_vs = None


def create_vectorstore(docs: list, embedding_model):
    """Wipe old index and build fresh."""
    global _vs
    from langchain_chroma import Chroma
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)
    _vs = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION,
    )
    print(f"[vectorstore] Built — {len(docs)} chunks.")
    return _vs


def load_vectorstore(embedding_model):
    """Load from disk. Singleton — never reloads unless reset."""
    global _vs
    if _vs is None:
        from langchain_chroma import Chroma
        _vs = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embedding_model,
            collection_name=COLLECTION,
        )
        print("[vectorstore] Loaded from disk.")
    return _vs


def reset_singleton():
    """Call after create_vectorstore so load_vectorstore picks up new index."""
    global _vs
    _vs = None


def vectorstore_exists() -> bool:
    return os.path.exists(CHROMA_DIR) and len(os.listdir(CHROMA_DIR)) > 0
