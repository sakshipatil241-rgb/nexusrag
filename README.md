# Nexus RAG — AI-Powered Document Search Assistant

> Upload your documents. Ask anything. Get precise, cited answers powered by Corrective RAG and Groq LLaMA 3.1.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Prerequisites](#5-prerequisites)
6. [Getting API Keys](#6-getting-api-keys)
7. [Local Setup](#7-local-setup)
8. [Running the App](#8-running-the-app)
9. [How to Use](#9-how-to-use)
10. [Deploy on Reflex Cloud](#10-deploy-on-reflex-cloud)
11. [Architecture](#11-architecture)
12. [Troubleshooting](#12-troubleshooting)
13. [Environment Variables](#13-environment-variables)

---

## 1. Project Overview

**Nexus RAG** is a full-stack AI web application that lets users upload private documents
(PDF, TXT, CSV) and ask natural language questions. Answers are generated strictly from the
uploaded content using a **Corrective RAG** pipeline with zero hallucination design.

Each user has a private account with isolated document storage, vector search index, and
chat history.

---

## 2. Features

### Core RAG Features
| Feature | Description |
|---------|-------------|
| Semantic Search | Queries matched by meaning, not keywords |
| Corrective RAG | Auto rewrites query if retrieved context is insufficient |
| Source Attribution | Every answer shows exact source filenames |
| Answer Confidence | Green/Yellow/Grey badge — verified / not found / low |
| AI Follow-up Suggestions | 3 clickable follow-up questions after each answer |
| Copy Answer | One-click clipboard copy on every AI response |
| Zero Hallucination | temperature=0, strict prompt rules, source-labeled chunks |

### Document Management
| Feature | Description |
|---------|-------------|
| Multi-format Upload | PDF, TXT, CSV chunked and indexed instantly |
| Document Stats | File size (KB) and segment count per file |
| AI Document Summary | Click "Generate summary" for 3-5 sentence AI summary |
| Delete All Documents | Wipe all files and vector index in one click |

### User Authentication
| Feature | Description |
|---------|-------------|
| Register / Login | Secure accounts with bcrypt-hashed passwords |
| Per-user Isolation | Each user's documents, index, and history are fully private |
| Session Persistence | Login state in localStorage — stays logged in after refresh |
| User Profile | View stats and document list at /profile |
| Protected Routes | All pages redirect to /login if not authenticated |

### History
| Feature | Description |
|---------|-------------|
| Persistent History | All Q&A saved to disk, restored on restart |
| Live History Search | Filter past conversations by keyword |
| Confidence Dot | Visual indicator per history entry |

---

## 3. Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Reflex (reflex.dev) | Python to React full-stack framework |
| LLM | Groq + LLaMA 3.1 8B | Sub-second AI inference |
| Embeddings | HuggingFace all-MiniLM-L6-v2 | Local CPU sentence embeddings |
| Vector DB | ChromaDB | Local persistent vector store |
| RAG | LangChain | Corrective RAG orchestration |
| Auth | bcrypt | Password hashing |
| Document Loaders | PyPDF, TextLoader, CSVLoader | PDF / TXT / CSV ingestion |

---

## 4. Project Structure

```
NexusRAG/
├── rxconfig.py                     Reflex config (plugins=[] suppresses warnings)
├── requirements.txt                All Python dependencies
├── .env.example                    Copy to .env and fill in API keys
├── .python-version                 Pins Python 3.11.0 for deployment
├── .gitignore
├── README.md
├── assets/
│   └── styles/global.css           Root CSS (Reflex requirement)
└── RAG_Project/                    cd HERE before running reflex
    ├── RAG_Project.py              App entry point + background warmup
    ├── assets/styles/global.css    Inner copy (required by Reflex)
    ├── auth/
    │   ├── __init__.py
    │   └── user_db.py              User DB: create/verify/stats (bcrypt)
    ├── components/
    │   ├── navbar.py               Auth-aware navbar with user avatar
    │   └── footer.py
    ├── pages/
    │   ├── home.py                 Landing page        /
    │   ├── login.py                Sign in             /login
    │   ├── register.py             Create account      /register
    │   ├── upload.py               Upload + stats      /upload
    │   ├── chat.py                 Chat interface      /chat
    │   ├── history.py              Q&A history         /history
    │   ├── profile.py              User profile        /profile
    │   └── about.py                About page          /about
    ├── rag/
    │   ├── loader.py               PDF/TXT/CSV to LangChain chunks
    │   ├── embeddings.py           HuggingFace MiniLM singleton
    │   ├── vectorstore.py          Per-user ChromaDB cache
    │   └── corrective_rag.py       Full corrective RAG pipeline
    └── states/
        ├── auth_state.py           Login/Register/Logout/Session
        └── rag_state.py            RAG state with per-user storage
```

### Per-user data layout (created at runtime inside RAG_Project/)

```
users/
├── users.json                      All accounts (bcrypt hashed passwords)
├── abc123def456/                   User 1 private folder
│   ├── data/                       Uploaded documents
│   ├── chroma_db/                  Vector index
│   └── history.json                Chat history
└── xyz789ghi012/                   User 2 private folder
    ├── data/
    ├── chroma_db/
    └── history.json
```

---

## 5. Prerequisites

- Python 3.11 (required — 3.12+ has compatibility issues)
- Node.js 18+ (Reflex uses it internally to compile the frontend)
- Git
- A Groq API key (free) — for LLaMA 3.1 inference
- A HuggingFace token (free) — for downloading the embedding model

---

## 6. Getting API Keys

### Groq API Key
1. Go to https://console.groq.com
2. Sign up for a free account
3. Click API Keys in the left sidebar
4. Click Create API Key — copy it (starts with gsk_)

### HuggingFace Token
1. Go to https://huggingface.co/settings/tokens
2. Sign up / log in
3. Click New token, select Read access, copy it (starts with hf_)

Both are completely free. No credit card required.

---

## 7. Local Setup

### Step 1 — Extract the project

Extract the NexusRAG folder to your desired location, e.g.:
```
C:\Users\ADMIN\Desktop\C\NexusRAG\
```

### Step 2 — Create Python virtual environment

```cmd
cd NexusRAG\RAG_Project
python -m venv venv
```

### Step 3 — Activate virtual environment

Windows:
```cmd
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

Your terminal prompt should show (venv).

### Step 4 — Install dependencies

```cmd
pip install -r ..\requirements.txt
```

This installs all packages including PyTorch, ChromaDB, LangChain (~2GB). Takes 5-10 minutes.

### Step 5 — Create .env file

Windows:
```cmd
copy ..\env.example .env
```

Mac / Linux:
```bash
cp ../env.example .env
```

Open .env in any text editor and fill in:
```
GROQ_API_KEY=gsk_your_actual_groq_key_here
HUGGINGFACEHUB_API_TOKEN=hf_your_actual_hf_token_here
```

### Step 6 — Initialize Reflex

```cmd
reflex init --template blank
```

You should see: Success: Initialized RAG_Project

---

## 8. Running the App

```cmd
cd NexusRAG\RAG_Project
venv\Scripts\activate
reflex run
```

Open your browser at: http://localhost:3000

To stop the app: press Ctrl+C

### Every restart (quick command)
```cmd
cd NexusRAG\RAG_Project && venv\Scripts\activate && reflex run
```

---

## 9. How to Use

### Create an Account
1. Go to http://localhost:3000/register
2. Enter display name (optional), username (min 3 chars), password (min 6 chars)
3. Confirm password and click Create Account
4. Go to /login and sign in

### Upload Documents
1. Go to Upload in the navbar (or http://localhost:3000/upload)
2. Drag and drop or click to select PDF, TXT, or CSV files
3. Click Upload & Index Documents
4. Wait for the status: "X file(s) processed (Y segments)"
5. Optionally click Generate summary on any file for an AI summary of that file

### Chat with Your Documents
1. Go to Chat in the navbar
2. Type any question about your uploaded documents
3. Press Enter or click the send button
4. Each answer shows:
   - The answer text
   - Confidence badge: green (verified from docs), yellow (not found), grey (low)
   - Source file chips showing which files were used
   - Copy button to copy the answer
   - 3 AI-generated follow-up question chips (click any to ask it)

### View History
1. Go to History in the navbar
2. Use the search box to filter past Q&A by keyword
3. Each entry shows a confidence dot

### User Profile
1. Click your display name in the top-right navbar
2. View your stats (questions asked, documents loaded)
3. See your uploaded documents list
4. Click Sign Out to log out

---

## 10. Deploy on Reflex Cloud

### Step 1 — Push to GitHub

```cmd
cd NexusRAG
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/nexusrag.git
git push -u origin main
```

### Step 2 — Deploy with API keys

```cmd
cd NexusRAG\RAG_Project
venv\Scripts\activate
reflex deploy --env GROQ_API_KEY=your_key --env HUGGINGFACEHUB_API_TOKEN=your_token
```

Follow the prompts:
- A browser will open — log in with your Reflex account
- Press Enter after logging in
- Confirm app creation when prompted

### Step 3 — Add/update keys via dashboard (if needed)

1. Go to https://build.reflex.dev
2. Click your app → Settings → Secrets
3. Add GROQ_API_KEY and HUGGINGFACEHUB_API_TOKEN
4. Click Restart

### Step 4 — Watch live logs

```cmd
reflex cloud apps status YOUR_APP_ID --watch
```

You should see:
```
[startup] Embedding model ready.
[startup] LLM client ready.
```

Note: On Reflex Cloud free tier, uploaded documents reset after each restart.
For persistent storage across restarts, use a paid tier with disk storage.

---

## 11. Architecture

### Corrective RAG Pipeline

```
User Query
    |
    v
1. RETRIEVE — MMR search, top-4 diverse chunks
    |
    v
2. EVALUATE — LLM checks: "Does context answer the question?"
    |               YES -> proceed   |   NO -> rewrite query -> re-retrieve
    v
3. GENERATE — LLaMA 3.1 8B at temperature=0
              Strict prompt: answer ONLY from retrieved context
    |
    v
4. CONFIDENCE — NOT_FOUND prefix -> yellow badge, else green
    |
    v
5. SUGGESTIONS — Generate 3 follow-up questions
    |
    v
Response: answer + sources + confidence + suggestions
```

### Key Design Decisions

**Per-user isolation:** Every user gets users/{user_id}/ with their own data/, chroma_db/,
and history.json. No user can access another's documents.

**Singletons:** The embedding model and per-user vectorstores are module-level singletons
loaded once and reused. No reloading on page navigation.

**Auth session:** rx.LocalStorage with named keys persists login across page refreshes
without a database.

**Cross-state user_id pattern:** RAGState.current_user_id is set via
RAGState.set_current_user(AuthState.user_id) on every page mount. This avoids the async
get_state() bug (calling .user_id on a coroutine crashes the handler).

**Page mount pattern used on every protected page:**
```python
on_mount=[
    AuthState.require_auth,
    RAGState.set_active_page("page_name"),
    RAGState.set_current_user(AuthState.user_id),
    RAGState.check_existing_index(),
]
```

---

## 12. Troubleshooting

### SitemapPlugin warnings appear on startup
Normal and harmless. Suppressed via plugins=[] in rxconfig.py.

### Error: cannot import name 'run_corrective_rag'
Fixed in this version. Check rag/__init__.py exports run_corrective_rag_vs.

### Error: coroutine object has no attribute 'user_id'
Fixed in this version. Caused by using get_state() (async) in a sync handler.
Solution: current_user_id field set on mount via set_current_user().

### Error: No module named 'langchain_text_splitters'
```cmd
pip install langchain-text-splitters>=0.3.0
```

### Chat shows "No documents loaded" after restart
Normal on Reflex Cloud free tier. Locally, check_existing_index() on mount
restores state from disk automatically.

### Groq API error on chat
Check .env file has GROQ_API_KEY=gsk_... with no spaces.
Restart reflex after editing .env.

### Upload fails: "No text extracted"
The file may be a scanned image PDF (not supported — needs OCR).
Try uploading a .txt file first to verify the pipeline.

### First startup takes 2-3 minutes
Normal — HuggingFace embedding model downloads on first run. Subsequent
starts are instant (model cached locally in venv).

### Windows: venv\Scripts\activate fails in PowerShell
Run in Command Prompt. Or allow scripts in PowerShell:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### UNEXPECTED key warning from BertModel
Safe to ignore. This is a benign warning from the HuggingFace model loader.

---

## 13. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GROQ_API_KEY | Yes | Groq API key for LLaMA 3.1 inference (starts with gsk_) |
| HUGGINGFACEHUB_API_TOKEN | Recommended | HuggingFace token for higher download rate limits |

---

## Dependencies (requirements.txt)

```
reflex>=0.6.0                     Full-stack Python web framework
langchain>=0.3.0                  RAG orchestration
langchain-community>=0.3.0        Document loaders
langchain-chroma>=0.1.4           ChromaDB integration
langchain-huggingface>=0.0.3      HuggingFace embeddings
langchain-groq>=0.1.0             Groq LLM client
langchain-core>=0.3.0             LangChain core
langchain-text-splitters>=0.3.0   RecursiveCharacterTextSplitter
chromadb>=0.5.0                   Local vector database
sentence-transformers>=2.7.0      all-MiniLM-L6-v2 model
pypdf>=4.0.0                      PDF text extraction
python-dotenv>=1.0.0              .env file loading
bcrypt>=4.0.0                     Password hashing
pydantic>=2.0.0                   Data models
```

---

Built with Reflex | LangChain | Groq | ChromaDB | HuggingFace
