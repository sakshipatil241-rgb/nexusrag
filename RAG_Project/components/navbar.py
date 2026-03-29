import reflex as rx
from RAG_Project.states.rag_state  import RAGState
from RAG_Project.states.auth_state import AuthState

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"

IC = {
    "home":    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "upload":  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
    "chat":    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "history": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "about":   '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
}


def _nav_link(label: str, href: str, key: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.html(IC[key]),
            rx.text(label, font_size="0.84rem", font_weight="500"),
            spacing="2", align_items="center",
        ),
        href=href,
        class_name=rx.cond(
            RAGState.active_page == key,
            "nav-link-item nav-link-active",
            "nav-link-item",
        ),
        _hover={"text_decoration": "none"},
    )


def _index_status() -> rx.Component:
    return rx.hstack(
        rx.box(
            width="7px", height="7px", border_radius="50%",
            background=rx.cond(RAGState.vectorstore_ready,
                               "#22C55E", "#94A3B8"),
        ),
        rx.text(
            rx.cond(RAGState.vectorstore_ready, "Ready", "No documents"),
            font_size="0.75rem", font_weight="500",
            color=rx.cond(RAGState.vectorstore_ready, "#15803D", "#64748B"),
        ),
        spacing="2", align_items="center",
        padding="5px 12px", border_radius="20px",
        background=rx.cond(RAGState.vectorstore_ready, "#F0FDF4", "#F8FAFC"),
        border=rx.cond(RAGState.vectorstore_ready,
                       "1px solid #BBF7D0", "1px solid #E2E8F0"),
    )


def _user_menu() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        rx.hstack(
            _index_status(),
            # User avatar + name → profile
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.text(AuthState.initials, font_size="0.72rem",
                                font_weight="800", color="white",
                                font_family=FONT),
                        width="30px", height="30px", border_radius="50%",
                        background="linear-gradient(135deg, #2563EB, #4F46E5)",
                        display="flex", align_items="center",
                        justify_content="center",
                        box_shadow="0 1px 6px rgba(37,99,235,0.3)",
                        flex_shrink="0",
                    ),
                    rx.text(AuthState.display_name, font_size="0.82rem",
                            font_weight="600", color="#0F172A",
                            max_width="100px"),
                    spacing="2", align_items="center",
                    padding="4px 10px 4px 4px",
                    border_radius="20px",
                    border="1px solid #E2E8F0",
                    background="white",
                    _hover={"border_color": "#BFDBFE",
                            "background": "#F8FAFC"},
                    transition="all 0.15s ease",
                ),
                href="/profile",
                _hover={"text_decoration": "none"},
            ),
            # Sign out
            rx.box(
                rx.html('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'),
                on_click=AuthState.logout,
                cursor="pointer", padding="7px 10px",
                border_radius="8px", color="#94A3B8",
                border="1px solid #E2E8F0", background="white",
                display="flex", align_items="center",
                _hover={"color": "#DC2626", "border_color": "#FECACA",
                        "background": "#FFF5F5"},
                transition="all 0.18s ease",
                title="Sign out",
            ),
            spacing="2", align_items="center",
        ),
        # Not logged in
        rx.hstack(
            rx.link(
                rx.text("Sign In", font_size="0.84rem", font_weight="500",
                        color="#64748B"),
                href="/login",
                class_name="nav-link-item",
                _hover={"text_decoration": "none"},
            ),
            rx.link(
                rx.text("Get Started", font_size="0.84rem",
                        font_weight="600"),
                href="/register",
                class_name="nexus-cta-btn",
                _hover={"text_decoration": "none"},
            ),
            spacing="2", align_items="center",
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.text("N", font_size="0.85rem", font_weight="800",
                                color="white", font_family=FONT),
                        class_name="nexus-logo-icon",
                    ),
                    rx.text("Nexus", font_size="1rem", font_weight="800",
                            color="#0F172A", letter_spacing="-0.02em",
                            font_family=FONT),
                    rx.text("RAG", class_name="nexus-logo-badge"),
                    spacing="2", align_items="center",
                ),
                href="/", _hover={"text_decoration": "none"},
            ),
            # Nav links
            rx.hstack(
                _nav_link("Home",    "/",        "home"),
                _nav_link("Upload",  "/upload",  "upload"),
                _nav_link("Chat",    "/chat",    "chat"),
                _nav_link("History", "/history", "history"),
                _nav_link("About",   "/about",   "about"),
                spacing="1",
            ),
            # Right side — user menu
            _user_menu(),
            justify="between", align_items="center", width="100%",
        ),
        class_name="nexus-nav",
    )
