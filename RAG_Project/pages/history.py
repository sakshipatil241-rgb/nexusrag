import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.rag_state  import RAGState
from RAG_Project.states.auth_state import AuthState
from RAG_Project.states.rag_state  import RAGState, QAPair

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


def _confidence_dot(confidence: str) -> rx.Component:
    return rx.cond(
        confidence == "high",
        rx.box(width="8px", height="8px", border_radius="50%",
               background="#22C55E", flex_shrink="0",
               title="Verified from documents"),
        rx.cond(
            confidence == "not_found",
            rx.box(width="8px", height="8px", border_radius="50%",
                   background="#F59E0B", flex_shrink="0",
                   title="Not found in documents"),
            rx.box(width="8px", height="8px", border_radius="50%",
                   background="#CBD5E1", flex_shrink="0"),
        ),
    )


def qa_card(pair: QAPair) -> rx.Component:
    return rx.box(
        # Question
        rx.box(
            rx.hstack(
                rx.box(
                    rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'),
                    width="24px", height="24px", border_radius="6px",
                    background="#F1F5F9", border="1px solid #E2E8F0",
                    display="flex", align_items="center",
                    justify_content="center", flex_shrink="0",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("You", font_size="0.65rem", font_weight="700",
                                color="#64748B", letter_spacing="0.06em"),
                        rx.text(pair.timestamp, font_size="0.65rem",
                                color="#CBD5E1"),
                        rx.text(pair.date, font_size="0.65rem",
                                color="#CBD5E1"),
                        spacing="2",
                    ),
                    rx.text(pair.question, font_size="0.9rem",
                            font_weight="600", color="#0F172A",
                            line_height="1.5"),
                    spacing="1", align_items="start",
                ),
                spacing="3", align_items="flex-start",
            ),
            padding="14px 18px", background="#F8FAFC",
            border_bottom="1px solid #E2E8F0",
        ),

        # Answer
        rx.box(
            rx.hstack(
                rx.box(
                    rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>'),
                    width="24px", height="24px", border_radius="6px",
                    background="linear-gradient(135deg, #2563EB, #4F46E5)",
                    display="flex", align_items="center",
                    justify_content="center", flex_shrink="0",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Nexus", font_size="0.65rem",
                                font_weight="700", color="#2563EB",
                                letter_spacing="0.06em"),
                        _confidence_dot(pair.confidence),
                        spacing="2", align_items="center",
                    ),
                    rx.text(pair.answer, font_size="0.875rem",
                            color="#374151", line_height="1.7",
                            white_space="pre-wrap"),
                    spacing="1", align_items="start",
                ),
                spacing="3", align_items="flex-start",
            ),
            padding="14px 18px",
        ),

        # Sources
        rx.cond(
            pair.sources.length() > 0,
            rx.box(
                rx.hstack(
                    rx.text("Sources:", font_size="0.7rem",
                            font_weight="700", color="#64748B"),
                    rx.foreach(
                        pair.sources,
                        lambda s: rx.box(
                            rx.hstack(
                                rx.html('<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
                                rx.text(s, font_size="0.7rem",
                                        font_weight="600"),
                                spacing="1", align_items="center",
                            ),
                            padding="3px 9px", border_radius="5px",
                            background="#F0FDF4",
                            border="1px solid #BBF7D0", color="#15803D",
                        ),
                    ),
                    spacing="2", align_items="center", flex_wrap="wrap",
                ),
                padding="10px 18px", border_top="1px solid #F1F5F9",
            ),
            rx.box(),
        ),

        border_radius="12px", border="1.5px solid #E2E8F0",
        overflow="hidden", box_shadow="0 1px 4px rgba(0,0,0,0.05)",
        width="100%",
    )


@rx.page(route="/history", title="History — Nexus RAG")
def history() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("Search History", font_size="1.5rem",
                            font_weight="800", color="#0F172A",
                            letter_spacing="-0.025em", font_family=FONT),
                    rx.text(
                        rx.cond(
                            RAGState.history.length() > 0,
                            "All questions and answers — saved across sessions",
                            "No history yet",
                        ),
                        font_size="0.82rem", color="#94A3B8",
                    ),
                    spacing="1", align_items="start",
                ),
                rx.hstack(
                    rx.link(
                        rx.box(
                            rx.text("Continue Chat", font_size="0.8rem",
                                    font_weight="600", color="white"),
                            padding="8px 18px", border_radius="8px",
                            background="linear-gradient(135deg, #2563EB, #4F46E5)",
                            box_shadow="0 2px 8px rgba(37,99,235,0.3)",
                            cursor="pointer",
                        ),
                        href="/chat", _hover={"text_decoration": "none"},
                    ),
                    rx.box(
                        rx.text("Clear All", font_size="0.8rem",
                                color="#94A3B8", font_weight="500"),
                        on_click=RAGState.clear_history,
                        padding="8px 18px", border_radius="8px",
                        border="1.5px solid #E2E8F0", background="white",
                        cursor="pointer",
                        _hover={"color": "#DC2626",
                                "border_color": "#FECACA"},
                        transition="all 0.18s ease",
                    ),
                    spacing="2",
                ),
                justify="between", align_items="center",
                width="100%", margin_bottom="24px",
            ),

            # Stats row
            rx.cond(
                RAGState.history.length() > 0,
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text(RAGState.total_questions,
                                    font_size="1.6rem", font_weight="800",
                                    color="#0F172A", font_family=FONT),
                            rx.text("Questions asked", font_size="0.72rem",
                                    color="#64748B"),
                            spacing="0", align_items="center",
                        ),
                        padding="18px 28px", border_radius="10px",
                        background="white", border="1.5px solid #E2E8F0",
                        text_align="center",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(RAGState.doc_count,
                                    font_size="1.6rem", font_weight="800",
                                    color="#0F172A", font_family=FONT),
                            rx.text("Documents loaded", font_size="0.72rem",
                                    color="#64748B"),
                            spacing="0", align_items="center",
                        ),
                        padding="18px 28px", border_radius="10px",
                        background="white", border="1.5px solid #E2E8F0",
                        text_align="center",
                    ),
                    spacing="3", margin_bottom="24px",
                ),
                rx.box(),
            ),

            # Search filter
            rx.cond(
                RAGState.history.length() > 0,
                rx.box(
                    rx.input(
                        placeholder="Search questions and answers...",
                        value=RAGState.history_search,
                        on_change=RAGState.set_history_search,
                        font_size="0.875rem", background="white",
                        color="#0F172A", border="1.5px solid #E2E8F0",
                        border_radius="9px", padding="10px 16px",
                        width="100%",
                        _placeholder={"color": "#94A3B8"},
                        _focus={
                            "border_color": "#3B82F6", "outline": "none",
                            "box_shadow": "0 0 0 3px rgba(37,99,235,0.1)",
                        },
                        font_family=FONT,
                    ),
                    margin_bottom="20px",
                ),
                rx.box(),
            ),

            # Empty state
            rx.cond(
                RAGState.history.length() == 0,
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.html('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'),
                            width="52px", height="52px", border_radius="14px",
                            background="#F1F5F9", border="1px solid #E2E8F0",
                            display="flex", align_items="center",
                            justify_content="center",
                        ),
                        rx.text("No search history yet",
                                font_size="1rem", font_weight="700",
                                color="#374151", font_family=FONT),
                        rx.text("Questions you ask will appear here.",
                                font_size="0.84rem", color="#94A3B8",
                                text_align="center"),
                        rx.link(
                            rx.box(
                                rx.text("Go to Chat", font_size="0.82rem",
                                        color="#2563EB", font_weight="600"),
                                padding="9px 20px", border_radius="8px",
                                border="1.5px solid #BFDBFE",
                                background="#EFF6FF", cursor="pointer",
                                _hover={"background": "#DBEAFE"},
                            ),
                            href="/chat",
                            _hover={"text_decoration": "none"},
                        ),
                        spacing="4", align_items="center",
                    ),
                    padding="72px 0", display="flex",
                    flex_direction="column", align_items="center",
                ),
                # Q&A cards (filtered)
                rx.cond(
                    RAGState.filtered_history.length() == 0,
                    rx.box(
                        rx.text("No results match your search.",
                                font_size="0.9rem", color="#94A3B8",
                                text_align="center"),
                        padding="40px 0",
                    ),
                    rx.vstack(
                        rx.foreach(RAGState.filtered_history, qa_card),
                        spacing="4", width="100%",
                    ),
                ),
            ),

            class_name="page-content",
        ),
        footer(),
        on_mount=[AuthState.require_auth, RAGState.set_active_page("history"), RAGState.set_current_user(AuthState.user_id), RAGState.check_existing_index()],
        background="#F8FAFC", min_height="100vh", font_family=FONT,
    )
