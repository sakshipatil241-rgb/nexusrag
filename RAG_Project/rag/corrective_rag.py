"""
Corrective RAG — per-user vectorstore support.
run_corrective_rag_vs() accepts a pre-loaded vectorstore object
so each user's isolated index is used.
"""
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

_executor   = ThreadPoolExecutor(max_workers=4)
_llm_client = None


def get_llm():
    global _llm_client
    if _llm_client is None:
        from langchain_groq import ChatGroq
        key = os.getenv("GROQ_API_KEY", "").strip()
        if not key:
            raise ValueError("GROQ_API_KEY not set. Add it to .env and restart.")
        _llm_client = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            api_key=key,
            max_tokens=1024,
        )
        print("[llm] Groq client ready.")
    return _llm_client


def _source(doc) -> str:
    return os.path.basename(
        doc.metadata.get("source",
        doc.metadata.get("file_path", "Unknown"))
    )


def _fmt(docs) -> tuple[str, list[str]]:
    parts = []
    for i, doc in enumerate(docs, 1):
        parts.append(f"[Source {i}: {_source(doc)}]\n{doc.page_content}")
    ctx  = "\n\n---\n\n".join(parts)
    srcs = list(dict.fromkeys(_source(d) for d in docs))
    return ctx, srcs


def _pipeline(query: str, vs) -> dict:
    """Core RAG pipeline using a provided vectorstore."""
    llm = get_llm()

    retriever = vs.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "lambda_mult": 0.6},
    )

    docs = retriever.invoke(query)
    if not docs:
        return {
            "answer": "No relevant content found. Try rephrasing.",
            "sources": [], "confidence": "low", "suggestions": [],
        }

    ctx, srcs = _fmt(docs)

    # Relevance check
    try:
        rel = llm.invoke(
            f"Does this context answer: '{query}'?\n"
            f"Context (500 chars): {ctx[:500]}\nYES or NO only."
        ).content.strip().upper()
    except Exception:
        rel = "YES"

    # Rewrite if not relevant
    if rel.startswith("NO"):
        try:
            better = llm.invoke(
                f"Rewrite for better search. Return ONLY the new query.\n"
                f"Original: {query}"
            ).content.strip()
            new_docs = retriever.invoke(better)
            if new_docs:
                docs, ctx, srcs = new_docs, *_fmt(new_docs)
        except Exception:
            pass

    # Generate answer
    raw = llm.invoke(
        f"""You are a precise document assistant. Answer using ONLY the context below.

RULES:
1. Use ONLY information from the context
2. Never use your training data
3. If not in context: say "NOT_FOUND: The documents do not contain this."
4. Be clear and concise. Use bullets for lists.
5. Never mention "context" or "documents" in your answer

Context:
{ctx}

Question: {query}
Answer:"""
    ).content.strip()

    if raw.startswith("NOT_FOUND:"):
        answer     = raw.replace("NOT_FOUND:", "").strip()
        confidence = "not_found"
    else:
        answer     = raw
        confidence = "high"

    # Follow-up suggestions
    suggestions = []
    if confidence == "high":
        try:
            sug = llm.invoke(
                f"Give 3 short follow-up questions based on this Q&A.\n"
                f"One per line. No bullets or numbers.\n"
                f"Q: {query}\nA: {answer[:300]}"
            ).content.strip()
            suggestions = [
                s.strip().lstrip("•-123456789. ")
                for s in sug.split("\n")
                if s.strip() and len(s.strip()) > 10
            ][:3]
        except Exception:
            pass

    return {
        "answer": answer, "sources": srcs,
        "confidence": confidence, "suggestions": suggestions,
    }


def _summarise(filename: str, data_dir: str) -> str:
    import shutil, tempfile
    from RAG_Project.rag.loader import load_documents

    fpath = os.path.join(data_dir, filename)
    if not os.path.exists(fpath):
        return "File not found."
    tmp = tempfile.mkdtemp()
    try:
        shutil.copy(fpath, os.path.join(tmp, filename))
        docs = load_documents(tmp)
        if not docs:
            return "Could not extract text."
        content = "\n".join(d.page_content for d in docs[:8])[:3000]
        return get_llm().invoke(
            f"Write a 3-5 sentence summary of this document.\n\n{content}\n\nSummary:"
        ).content.strip()
    except Exception as e:
        return f"Could not summarise: {e}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


async def run_corrective_rag_vs(query: str, vs) -> dict:
    """Async wrapper — takes pre-loaded vectorstore (per-user)."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _executor, _pipeline, query, vs
    )


async def summarise_document(filename: str, data_dir: str = "./data") -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _executor, _summarise, filename, data_dir
    )
