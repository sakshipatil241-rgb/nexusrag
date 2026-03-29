"""
Nexus RAG — App entry point.
Background warmup thread pre-loads all heavy singletons at startup.
"""
import reflex as rx
import threading

from RAG_Project.pages.home     import home
from RAG_Project.pages.login    import login
from RAG_Project.pages.register import register
from RAG_Project.pages.upload   import upload
from RAG_Project.pages.chat     import chat
from RAG_Project.pages.history  import history
from RAG_Project.pages.profile  import profile
from RAG_Project.pages.about    import about


def _warmup():
    try:
        from RAG_Project.rag.embeddings import get_embedding_model
        emb = get_embedding_model()
        print("[startup] Embedding model ready.")
    except Exception as e:
        print(f"[startup] Embedding: {e}")
        return
    try:
        from RAG_Project.rag.corrective_rag import get_llm
        get_llm()
        print("[startup] LLM client ready.")
    except Exception as e:
        print(f"[startup] LLM: {e}")


threading.Thread(target=_warmup, daemon=True).start()


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap",
        "styles/global.css",
    ],
    style={
        "font_family": "'Plus Jakarta Sans', 'Inter', sans-serif",
        "background": "#F8FAFC",
    },
)
