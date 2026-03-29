import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.auth_state import AuthState
from RAG_Project.states.rag_state  import RAGState

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


@rx.page(route="/profile", title="Profile — Nexus RAG")
def profile() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                # Avatar + name
                rx.vstack(
                    rx.box(
                        rx.text(AuthState.initials,
                                font_size="1.5rem", font_weight="800",
                                color="white", font_family=FONT),
                        width="80px", height="80px", border_radius="50%",
                        background="linear-gradient(135deg, #2563EB, #4F46E5)",
                        display="flex", align_items="center",
                        justify_content="center",
                        box_shadow="0 4px 20px rgba(37,99,235,0.35)",
                    ),
                    rx.text(AuthState.display_name, font_size="1.5rem",
                            font_weight="800", color="#0F172A",
                            letter_spacing="-0.025em", font_family=FONT),
                    rx.text("@" + AuthState.username, font_size="0.9rem",
                            color="#64748B"),
                    rx.hstack(
                        rx.html('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.5"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'),
                        rx.text("Member since " + AuthState.created_at[:10],
                                font_size="0.8rem", color="#94A3B8"),
                        spacing="2", align_items="center",
                    ),
                    spacing="3", align_items="center",
                    padding="48px 0 32px",
                ),

                # Stats cards
                rx.hstack(
                    _stat_card("Questions Asked", RAGState.total_questions,
                               '#2563EB', '#EFF6FF', '#BFDBFE',
                               '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'),
                    _stat_card("Documents Loaded", RAGState.doc_count,
                               '#4F46E5', '#EEF2FF', '#C7D2FE',
                               '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
                    _stat_card("History Entries", RAGState.total_questions,
                               '#059669', '#ECFDF5', '#A7F3D0',
                               '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'),
                    spacing="4", width="100%",
                    flex_wrap="wrap",
                ),

                # Your documents
                rx.cond(
                    RAGState.doc_stats.length() > 0,
                    rx.box(
                        rx.text("Your Documents", font_size="1.1rem",
                                font_weight="700", color="#0F172A",
                                font_family=FONT, margin_bottom="16px"),
                        rx.vstack(
                            rx.foreach(
                                RAGState.doc_stats,
                                lambda ds: rx.hstack(
                                    rx.html('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
                                    rx.text(ds.filename, font_size="0.875rem",
                                            color="#374151", flex="1"),
                                    rx.text(f"{ds.size_kb} KB",
                                            font_size="0.75rem",
                                            color="#94A3B8"),
                                    spacing="3", align_items="center",
                                    padding="10px 16px",
                                    border_bottom="1px solid #F1F5F9",
                                    width="100%",
                                ),
                            ),
                            spacing="0", width="100%",
                        ),
                        background="white", border_radius="12px",
                        border="1.5px solid #E2E8F0",
                        overflow="hidden", width="100%",
                        margin_top="32px",
                    ),
                    rx.box(),
                ),

                # Actions
                rx.hstack(
                    rx.link(
                        rx.box(
                            rx.text("Go to Chat", font_size="0.84rem",
                                    font_weight="600", color="white"),
                            padding="10px 22px", border_radius="9px",
                            background="linear-gradient(135deg, #2563EB, #4F46E5)",
                            cursor="pointer",
                            box_shadow="0 2px 8px rgba(37,99,235,0.3)",
                        ),
                        href="/chat", _hover={"text_decoration": "none"},
                    ),
                    rx.box(
                        rx.text("Sign Out", font_size="0.84rem",
                                font_weight="500", color="#DC2626"),
                        on_click=AuthState.logout,
                        padding="10px 22px", border_radius="9px",
                        border="1.5px solid #FECACA", background="#FFF5F5",
                        cursor="pointer",
                        _hover={"background": "#FEE2E2"},
                        transition="all 0.18s ease",
                    ),
                    spacing="3", margin_top="32px",
                ),

                spacing="0", align_items="center",
                max_width="700px", margin="0 auto",
            ),
            class_name="page-content",
        ),
        footer(),
        on_mount=[AuthState.require_auth, RAGState.set_active_page("profile"), RAGState.set_current_user(AuthState.user_id), RAGState.check_existing_index()],
        background="#F8FAFC", min_height="100vh", font_family=FONT,
    )


def _stat_card(label, value, color, bg, border, icon_svg):
    return rx.box(
        rx.hstack(
            rx.box(rx.html(icon_svg), width="40px", height="40px",
                   border_radius="10px", background=bg,
                   border=f"1px solid {border}",
                   display="flex", align_items="center",
                   justify_content="center"),
            rx.vstack(
                rx.text(value, font_size="1.6rem", font_weight="800",
                        color=color, font_family=FONT),
                rx.text(label, font_size="0.75rem", color="#64748B"),
                spacing="0", align_items="start",
            ),
            spacing="3", align_items="center",
        ),
        padding="20px 24px", border_radius="12px",
        background="white", border="1.5px solid #E2E8F0",
        flex="1", min_width="180px",
    )
