"""
RAG State — per-user isolated storage.

KEY FIX: user_id is now stored directly as a state var (synced from AuthState
via on_mount) instead of cross-state lookup via get_state() which is async
and cannot be used in sync event handlers.
"""
import reflex as rx
import os
import json
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


# ── Data models ───────────────────────────────────────────────────────────────

class Message(BaseModel):
    role:        str
    content:     str
    sources:     list[str] = []
    confidence:  str       = "high"
    suggestions: list[str] = []


class QAPair(BaseModel):
    question:    str
    answer:      str
    sources:     list[str] = []
    confidence:  str       = "high"
    suggestions: list[str] = []
    timestamp:   str       = ""
    date:        str       = ""


class DocStat(BaseModel):
    filename:    str
    size_kb:     float = 0.0
    chunks:      int   = 0
    summary:     str   = ""
    summarising: bool  = False


# ── Per-user path helpers ─────────────────────────────────────────────────────

def _data_dir(uid: str) -> str:
    d = f"./users/{uid}/data"
    os.makedirs(d, exist_ok=True)
    return d

def _chroma_dir(uid: str) -> str:
    return f"./users/{uid}/chroma_db"

def _history_file(uid: str) -> str:
    return f"./users/{uid}/history.json"

def _chroma_exists(uid: str) -> bool:
    d = _chroma_dir(uid)
    return os.path.exists(d) and len(os.listdir(d)) > 0

def _scan_files(uid: str) -> list[str]:
    d = _data_dir(uid)
    return sorted(f for f in os.listdir(d)
                  if f.lower().endswith((".pdf", ".txt", ".csv")))

def _file_kb(uid: str, fname: str) -> float:
    p = os.path.join(_data_dir(uid), fname)
    return round(os.path.getsize(p) / 1024, 1) if os.path.exists(p) else 0.0

def _save_history(uid: str, history: list[QAPair]) -> None:
    try:
        fpath = _history_file(uid)
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump([q.model_dump() for q in history], f,
                      ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[history] Save: {e}")

def _load_history(uid: str) -> list[QAPair]:
    fpath = _history_file(uid)
    if not os.path.exists(fpath):
        return []
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            return [QAPair(**item) for item in json.load(f)]
    except Exception as e:
        print(f"[history] Load: {e}")
        return []

def _to_messages(history: list[QAPair]) -> list[Message]:
    out = []
    for q in history:
        out.append(Message(role="user", content=q.question))
        out.append(Message(role="assistant", content=q.answer,
                           sources=q.sources, confidence=q.confidence,
                           suggestions=q.suggestions))
    return out


# ── Per-user vectorstore cache ────────────────────────────────────────────────

_vs_cache: dict[str, object] = {}

def _load_vs(uid: str, emb):
    if uid not in _vs_cache or _vs_cache[uid] is None:
        from langchain_chroma import Chroma
        _vs_cache[uid] = Chroma(
            persist_directory=_chroma_dir(uid),
            embedding_function=emb,
            collection_name="rag_documents",
        )
    return _vs_cache[uid]

def _create_vs(uid: str, docs: list, emb):
    import shutil
    from langchain_chroma import Chroma
    cdir = _chroma_dir(uid)
    if os.path.exists(cdir):
        shutil.rmtree(cdir)
    vs = Chroma.from_documents(
        documents=docs, embedding=emb,
        persist_directory=cdir, collection_name="rag_documents",
    )
    _vs_cache[uid] = vs
    print(f"[vs] Built {len(docs)} chunks for user {uid[:6]}")
    return vs

def _reset_vs(uid: str):
    _vs_cache.pop(uid, None)


# ── State ─────────────────────────────────────────────────────────────────────

class RAGState(rx.State):

    # ── Auth mirror — set from AuthState on every page mount ──────────────
    # This avoids the async get_state() lookup that caused the crash.
    current_user_id: str = ""

    # ── Chat ──────────────────────────────────────────────────────────────
    messages:          list[Message] = []
    history:           list[QAPair]  = []
    user_input:        str  = ""
    is_loading:        bool = False
    loading_status:    str  = ""
    error_message:     str  = ""

    # ── Upload ────────────────────────────────────────────────────────────
    upload_status:     str           = ""
    is_uploading:      bool          = False
    uploaded_files:    list[str]     = []
    doc_stats:         list[DocStat] = []
    vectorstore_ready: bool          = False
    total_chunks:      int           = 0

    # ── History filter ────────────────────────────────────────────────────
    history_search:    str  = ""

    # ── UI ────────────────────────────────────────────────────────────────
    active_page:       str  = "home"

    # ── Computed vars ─────────────────────────────────────────────────────
    @rx.var
    def filtered_history(self) -> list[QAPair]:
        if not self.history_search.strip():
            return self.history
        q = self.history_search.lower()
        return [h for h in self.history
                if q in h.question.lower() or q in h.answer.lower()]

    @rx.var
    def total_questions(self) -> int:
        return len(self.history)

    @rx.var
    def doc_count(self) -> int:
        return len(self.uploaded_files)

    # ── Set user_id mirror (called on every page mount) ───────────────────
    def set_current_user(self, uid: str):
        """Receive user_id from AuthState and store locally."""
        self.current_user_id = uid

    # ── Restore from disk ─────────────────────────────────────────────────
    def check_existing_index(self):
        """
        Restore per-user files/index/history from disk.
        Uses self.current_user_id (set via set_current_user) — no async lookup.
        """
        uid = self.current_user_id
        if not uid:
            return

        for f in _scan_files(uid):
            if f not in self.uploaded_files:
                self.uploaded_files = self.uploaded_files + [f]

        current_names = {ds.filename for ds in self.doc_stats}
        for f in _scan_files(uid):
            if f not in current_names:
                self.doc_stats = self.doc_stats + [
                    DocStat(filename=f, size_kb=_file_kb(uid, f))
                ]

        if _chroma_exists(uid):
            self.vectorstore_ready = True

        if not self.history:
            saved = _load_history(uid)
            if saved:
                self.history  = saved
                self.messages = _to_messages(saved)

    # ── Setters ───────────────────────────────────────────────────────────
    def set_user_input(self, v: str):    self.user_input    = v
    def set_active_page(self, p: str):   self.active_page   = p
    def set_history_search(self, v: str): self.history_search = v
    def use_suggestion(self, text: str): self.user_input    = text

    def clear_chat(self):
        self.messages = []
        self.error_message = ""
        self.loading_status = ""

    def clear_history(self):
        uid = self.current_user_id
        self.history = []
        self.messages = []
        self.error_message = ""
        if uid:
            try:
                f = _history_file(uid)
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

    def delete_all_documents(self):
        """Delete all uploaded files, wipe index, reset UI state."""
        uid = self.current_user_id
        if not uid:
            return
        import shutil
        try:
            for f in _scan_files(uid):
                os.remove(os.path.join(_data_dir(uid), f))
            cdir = _chroma_dir(uid)
            if os.path.exists(cdir):
                shutil.rmtree(cdir)
            _reset_vs(uid)
        except Exception as e:
            print(f"[delete] {e}")
        self.uploaded_files    = []
        self.doc_stats         = []
        self.vectorstore_ready = False
        self.total_chunks      = 0
        self.upload_status     = ""

    # ── Upload ────────────────────────────────────────────────────────────
    async def handle_upload(self, files: list[rx.UploadFile]):
        uid = self.current_user_id
        if not uid:
            self.upload_status = "Please log in first."
            return
        if not files:
            self.upload_status = "No files received."
            return

        self.is_uploading  = True
        self.error_message = ""
        self.upload_status = f"Saving {len(files)} file(s)..."
        yield

        try:
            data_dir = _data_dir(uid)
            for file in files:
                raw  = await file.read()
                name = file.filename
                with open(os.path.join(data_dir, name), "wb") as fp:
                    fp.write(raw)
                if name not in self.uploaded_files:
                    self.uploaded_files = self.uploaded_files + [name]
                    self.doc_stats = self.doc_stats + [
                        DocStat(filename=name, size_kb=_file_kb(uid, name))
                    ]
                self.upload_status = f"Saved: {name}"
                yield

            self.upload_status = "Processing documents..."
            yield

            from RAG_Project.rag.loader     import load_documents
            from RAG_Project.rag.embeddings import get_embedding_model

            docs = load_documents(data_dir)
            if not docs:
                self.upload_status = "No text extracted. Check files are not empty."
                self.is_uploading = False
                return

            self.upload_status = f"Building index ({len(docs)} segments)..."
            yield

            emb = get_embedding_model()
            _create_vs(uid, docs, emb)

            self.vectorstore_ready = True
            self.total_chunks      = len(docs)

            # Update chunk counts per file
            per_file   = max(1, len(docs) // max(1, len(files)))
            file_names = [f.filename for f in files]
            self.doc_stats = [
                DocStat(filename=ds.filename, size_kb=ds.size_kb,
                        chunks=per_file, summary=ds.summary)
                if ds.filename in file_names and ds.chunks == 0
                else ds
                for ds in self.doc_stats
            ]

            from RAG_Project.auth.user_db import update_user_stats
            update_user_stats(uid, docs_delta=len(files))

            self.upload_status = (
                f"{len(self.uploaded_files)} file(s) processed "
                f"({len(docs)} segments). You can now search."
            )

        except Exception as exc:
            self.upload_status = f"Failed: {exc}"
            self.error_message  = str(exc)
        finally:
            self.is_uploading = False

    # ── Document summary ──────────────────────────────────────────────────
    async def summarise_doc(self, filename: str):
        uid = self.current_user_id
        self.doc_stats = [
            DocStat(filename=ds.filename, size_kb=ds.size_kb,
                    chunks=ds.chunks, summary="Generating...",
                    summarising=True)
            if ds.filename == filename else ds
            for ds in self.doc_stats
        ]
        yield
        try:
            from RAG_Project.rag.corrective_rag import summarise_document
            summary = await summarise_document(filename, _data_dir(uid))
        except Exception as e:
            summary = f"Could not summarise: {e}"
        self.doc_stats = [
            DocStat(filename=ds.filename, size_kb=ds.size_kb,
                    chunks=ds.chunks, summary=summary, summarising=False)
            if ds.filename == filename else ds
            for ds in self.doc_stats
        ]

    # ── Ask ───────────────────────────────────────────────────────────────
    async def ask(self):
        uid   = self.current_user_id
        query = self.user_input.strip()
        if not query or not uid:
            return
        if not self.vectorstore_ready:
            self.error_message = "No documents loaded. Go to Upload first."
            return

        self.user_input     = ""
        self.is_loading     = True
        self.error_message  = ""
        self.loading_status = "Searching documents..."
        self.messages = self.messages + [Message(role="user", content=query)]
        yield

        try:
            self.loading_status = "Generating answer..."
            yield

            from RAG_Project.rag.embeddings     import get_embedding_model
            from RAG_Project.rag.corrective_rag import run_corrective_rag_vs

            emb    = get_embedding_model()
            vs     = _load_vs(uid, emb)
            result = await run_corrective_rag_vs(query, vs)

            self.loading_status = ""
            self.messages = self.messages + [
                Message(role="assistant",
                        content=result["answer"],
                        sources=result["sources"],
                        confidence=result["confidence"],
                        suggestions=result["suggestions"])
            ]

            import datetime
            now  = datetime.datetime.now()
            pair = QAPair(
                question=query, answer=result["answer"],
                sources=result["sources"], confidence=result["confidence"],
                suggestions=result["suggestions"],
                timestamp=now.strftime("%H:%M"),
                date=now.strftime("%d %b %Y"),
            )
            self.history = self.history + [pair]
            _save_history(uid, list(self.history))

            from RAG_Project.auth.user_db import update_user_stats
            update_user_stats(uid, questions_delta=1)

        except Exception as exc:
            self.loading_status = ""
            err = str(exc)
            if "GROQ_API_KEY" in err or "api_key" in err.lower():
                msg = "API key missing. Add GROQ_API_KEY to .env and restart."
            elif "429" in err or "rate" in err.lower():
                msg = "Rate limit reached. Wait a moment and try again."
            else:
                msg = f"Error: {err}"
            self.messages = self.messages + [
                Message(role="assistant", content=msg, confidence="low")
            ]
        finally:
            self.is_loading     = False
            self.loading_status = ""

    async def send_message(self):
        async for _ in self.ask():
            yield

    async def send_on_enter(self, key: str):
        if key == "Enter":
            async for _ in self.ask():
                yield
