import os


def load_documents(data_dir: str = "./data") -> list:
    """Load all PDF/TXT/CSV files and return chunked LangChain Documents."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    os.makedirs(data_dir, exist_ok=True)
    all_docs = []

    for fname in sorted(os.listdir(data_dir)):
        fpath = os.path.join(data_dir, fname)
        if not os.path.isfile(fpath):
            continue
        ext = fname.lower().rsplit(".", 1)[-1] if "." in fname else ""
        try:
            if ext == "pdf":
                from langchain_community.document_loaders import PyPDFLoader
                docs = PyPDFLoader(fpath).load()
            elif ext == "txt":
                from langchain_community.document_loaders import TextLoader
                docs = TextLoader(fpath, encoding="utf-8",
                                  autodetect_encoding=True).load()
            elif ext == "csv":
                from langchain_community.document_loaders import CSVLoader
                docs = CSVLoader(fpath).load()
            else:
                continue
            for d in docs:
                d.metadata["source"] = fname
            all_docs.extend(docs)
            print(f"[loader] Loaded: {fname} ({len(docs)} pages)")
        except Exception as e:
            print(f"[loader] Skipped {fname}: {e}")

    if not all_docs:
        return []

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
    ).split_documents(all_docs)
    print(f"[loader] Total: {len(all_docs)} pages → {len(chunks)} chunks")
    return chunks
