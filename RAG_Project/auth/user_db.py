"""
Simple file-based user database.
Stores users in ./users/users.json
Each user gets their own folder: ./users/{user_id}/
"""
import os
import json
import uuid
import datetime
import bcrypt

USERS_DIR  = "./users"
USERS_FILE = "./users/users.json"


def _load_db() -> dict:
    os.makedirs(USERS_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_db(db: dict) -> None:
    os.makedirs(USERS_DIR, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _user_dir(user_id: str) -> str:
    d = os.path.join(USERS_DIR, user_id)
    os.makedirs(d, exist_ok=True)
    return d


def create_user(username: str, password: str,
                display_name: str = "") -> dict:
    """
    Create a new user. Returns dict with success/error.
    Passwords are hashed with bcrypt before storage.
    """
    db = _load_db()
    uname = username.strip().lower()

    if not uname or len(uname) < 3:
        return {"ok": False, "error": "Username must be at least 3 characters."}
    if not password or len(password) < 6:
        return {"ok": False, "error": "Password must be at least 6 characters."}

    # Check unique
    for uid, u in db.items():
        if u["username"] == uname:
            return {"ok": False, "error": "Username already taken. Please choose another."}

    user_id = str(uuid.uuid4())[:12]
    hashed  = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db[user_id] = {
        "user_id":      user_id,
        "username":     uname,
        "display_name": display_name.strip() or username.strip(),
        "password_hash": hashed,
        "created_at":   datetime.datetime.now().isoformat(),
        "total_questions": 0,
        "total_docs":      0,
    }
    _save_db(db)

    # Create user directories
    _user_dir(user_id)
    os.makedirs(os.path.join(USERS_DIR, user_id, "data"), exist_ok=True)

    return {"ok": True, "user_id": user_id,
            "username": uname,
            "display_name": db[user_id]["display_name"],
            "created_at": db[user_id]["created_at"]}


def verify_user(username: str, password: str) -> dict:
    """
    Verify login credentials. Returns user dict on success.
    """
    db  = _load_db()
    uname = username.strip().lower()

    for uid, u in db.items():
        if u["username"] == uname:
            if bcrypt.checkpw(password.encode(), u["password_hash"].encode()):
                return {
                    "ok": True,
                    "user_id":      uid,
                    "username":     u["username"],
                    "display_name": u.get("display_name", u["username"]),
                    "created_at":   u.get("created_at", ""),
                }
            return {"ok": False, "error": "Incorrect password."}

    return {"ok": False, "error": "No account found with that username."}


def get_user(user_id: str) -> dict | None:
    db = _load_db()
    return db.get(user_id)


def user_exists(username: str) -> bool:
    db = _load_db()
    uname = username.strip().lower()
    return any(u["username"] == uname for u in db.values())


def get_user_stats(user_id: str) -> dict:
    db = _load_db()
    u  = db.get(user_id, {})
    return {
        "total_questions": u.get("total_questions", 0),
        "total_docs":      u.get("total_docs", 0),
        "created_at":      u.get("created_at", ""),
    }


def update_user_stats(user_id: str,
                      questions_delta: int = 0,
                      docs_delta: int = 0) -> None:
    db = _load_db()
    if user_id in db:
        db[user_id]["total_questions"] = (
            db[user_id].get("total_questions", 0) + questions_delta
        )
        db[user_id]["total_docs"] = (
            db[user_id].get("total_docs", 0) + docs_delta
        )
        _save_db(db)


def get_user_data_dir(user_id: str) -> str:
    d = os.path.join(USERS_DIR, user_id, "data")
    os.makedirs(d, exist_ok=True)
    return d


def get_user_chroma_dir(user_id: str) -> str:
    return os.path.join(USERS_DIR, user_id, "chroma_db")


def get_user_history_file(user_id: str) -> str:
    return os.path.join(USERS_DIR, user_id, "history.json")
