"""Module-level singleton — loads exactly once per Python process."""
import os

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        cache = os.environ.get("SENTENCE_TRANSFORMERS_HOME", None)
        if cache:
            os.makedirs(cache, exist_ok=True)
        print("[embeddings] Loading model...")
        _model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        print("[embeddings] Ready.")
    return _model


def prewarm():
    get_embedding_model()
