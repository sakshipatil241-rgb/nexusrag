"""
AuthState — login, register, logout, session via LocalStorage.
FIXED: rx.LocalStorage does NOT accept 'default=' keyword.
Use: field: str = rx.LocalStorage("")  (value only, no kwargs)
"""
import reflex as rx


class AuthState(rx.State):
    # ── Persisted in browser localStorage ─────────────────────────────────
    # CORRECT syntax: rx.LocalStorage("default_value") — no keyword args
    user_id:      str = rx.LocalStorage("")
    username:     str = rx.LocalStorage("")
    display_name: str = rx.LocalStorage("")
    created_at:   str = rx.LocalStorage("")

    # ── Form fields (in-memory only) ──────────────────────────────────────
    login_username:  str = ""
    login_password:  str = ""
    reg_username:    str = ""
    reg_password:    str = ""
    reg_confirm:     str = ""
    reg_display:     str = ""

    # ── UI state ──────────────────────────────────────────────────────────
    login_error:   str  = ""
    reg_error:     str  = ""
    reg_success:   str  = ""
    is_loading:    bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user_id != ""

    @rx.var
    def initials(self) -> str:
        name = self.display_name or self.username
        if not name:
            return "?"
        parts = name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return name[:2].upper()

    # ── Setters ───────────────────────────────────────────────────────────
    def set_login_username(self, v: str): self.login_username = v
    def set_login_password(self, v: str): self.login_password = v
    def set_reg_username(self, v: str):   self.reg_username   = v
    def set_reg_password(self, v: str):   self.reg_password   = v
    def set_reg_confirm(self, v: str):    self.reg_confirm    = v
    def set_reg_display(self, v: str):    self.reg_display    = v

    def clear_errors(self):
        self.login_error = ""
        self.reg_error   = ""
        self.reg_success = ""

    # ── Login ─────────────────────────────────────────────────────────────
    def do_login(self):
        self.login_error = ""
        if not self.login_username.strip():
            self.login_error = "Please enter your username."
            return
        if not self.login_password:
            self.login_error = "Please enter your password."
            return
        self.is_loading = True
        from RAG_Project.auth.user_db import verify_user
        result = verify_user(self.login_username.strip(), self.login_password)
        self.is_loading = False
        if result["ok"]:
            self.user_id      = result["user_id"]
            self.username     = result["username"]
            self.display_name = result["display_name"]
            self.created_at   = result.get("created_at", "")
            self.login_username = ""
            self.login_password = ""
            return rx.redirect("/chat")
        else:
            self.login_error = result["error"]

    def do_login_enter(self, key: str):
        if key == "Enter":
            return self.do_login()

    # ── Register ──────────────────────────────────────────────────────────
    def do_register(self):
        self.reg_error   = ""
        self.reg_success = ""
        if len(self.reg_username.strip()) < 3:
            self.reg_error = "Username must be at least 3 characters."
            return
        if len(self.reg_password) < 6:
            self.reg_error = "Password must be at least 6 characters."
            return
        if self.reg_password != self.reg_confirm:
            self.reg_error = "Passwords do not match."
            return
        self.is_loading = True
        from RAG_Project.auth.user_db import create_user
        result = create_user(
            username=self.reg_username.strip(),
            password=self.reg_password,
            display_name=self.reg_display.strip(),
        )
        self.is_loading = False
        if result["ok"]:
            self.reg_success  = "Account created! You can now sign in."
            self.reg_username = ""
            self.reg_password = ""
            self.reg_confirm  = ""
            self.reg_display  = ""
        else:
            self.reg_error = result["error"]

    # ── Logout ────────────────────────────────────────────────────────────
    def logout(self):
        self.user_id      = ""
        self.username     = ""
        self.display_name = ""
        self.created_at   = ""
        return rx.redirect("/login")

    # ── Guard ─────────────────────────────────────────────────────────────
    def require_auth(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
