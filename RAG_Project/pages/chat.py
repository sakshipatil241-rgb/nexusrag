import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.rag_state  import RAGState
from RAG_Project.states.auth_state import AuthState
from RAG_Project.states.rag_state  import RAGState, Message

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


def _source_chip(src: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.html('<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
            rx.text(src, font_size="0.7rem", font_weight="600"),
            spacing="1", align_items="center",
        ),
        padding="3px 9px", border_radius="5px",
        background="#F0FDF4", border="1px solid #BBF7D0",
        color="#15803D", margin_right="5px", margin_top="4px",
    )


def _confidence_badge(confidence: str) -> rx.Component:
    return rx.cond(
        confidence == "high",
        rx.box(
            rx.hstack(
                rx.box(width="6px", height="6px", border_radius="50%",
                       background="#22C55E"),
                rx.text("Verified from documents", font_size="0.68rem",
                        font_weight="600", color="#15803D"),
                spacing="2", align_items="center",
            ),
            padding="3px 8px", border_radius="5px",
            background="#F0FDF4", border="1px solid #BBF7D0",
            display="inline-flex", margin_top="6px",
        ),
        rx.cond(
            confidence == "not_found",
            rx.box(
                rx.hstack(
                    rx.box(width="6px", height="6px", border_radius="50%",
                           background="#F59E0B"),
                    rx.text("Not found in documents", font_size="0.68rem",
                            font_weight="600", color="#92400E"),
                    spacing="2", align_items="center",
                ),
                padding="3px 8px", border_radius="5px",
                background="#FFFBEB", border="1px solid #FDE68A",
                display="inline-flex", margin_top="6px",
            ),
            rx.box(
                rx.hstack(
                    rx.box(width="6px", height="6px", border_radius="50%",
                           background="#94A3B8"),
                    rx.text("Low confidence", font_size="0.68rem",
                            font_weight="600", color="#64748B"),
                    spacing="2", align_items="center",
                ),
                padding="3px 8px", border_radius="5px",
                background="#F8FAFC", border="1px solid #E2E8F0",
                display="inline-flex", margin_top="6px",
            ),
        ),
    )


def _suggestion_chip(text: str) -> rx.Component:
    return rx.box(
        rx.text(text, font_size="0.78rem", color="#2563EB", font_weight="500"),
        padding="5px 12px", border_radius="20px",
        background="#EFF6FF", border="1px solid #BFDBFE",
        cursor="pointer",
        on_click=RAGState.use_suggestion(text),
        _hover={"background": "#DBEAFE", "border_color": "#93C5FD"},
        transition="all 0.15s ease",
        margin_right="6px", margin_top="6px",
        display="inline-block",
    )


def _bot_bubble(msg: Message) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>'),
            width="28px", height="28px", border_radius="7px", flex_shrink="0",
            background="linear-gradient(135deg, #2563EB, #4F46E5)",
            display="flex", align_items="center", justify_content="center",
        ),
        rx.vstack(
            # Answer bubble
            rx.box(
                rx.text(msg.content, font_size="0.875rem", color="#0F172A",
                        line_height="1.7", white_space="pre-wrap"),
                padding="12px 16px", border_radius="12px 12px 12px 3px",
                background="white", border="1px solid #E2E8F0",
                box_shadow="0 1px 3px rgba(0,0,0,0.05)", max_width="640px",
            ),
            # Confidence badge
            _confidence_badge(msg.confidence),
            # Sources
            rx.cond(
                msg.sources.length() > 0,
                rx.hstack(
                    rx.foreach(msg.sources, _source_chip),
                    spacing="0", flex_wrap="wrap",
                ),
                rx.box(),
            ),
            # Copy button
            rx.box(
                rx.hstack(
                    rx.html('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'),
                    rx.text("Copy answer", font_size="0.7rem", font_weight="500"),
                    spacing="1", align_items="center",
                ),
                padding="4px 10px", border_radius="5px",
                background="#F8FAFC", border="1px solid #E2E8F0",
                cursor="pointer", color="#64748B", margin_top="6px",
                display="inline-flex",
                on_click=[
                    rx.set_clipboard(msg.content),
                ],
                _hover={"background": "#F1F5F9", "color": "#2563EB",
                        "border_color": "#BFDBFE"},
                transition="all 0.15s ease",
            ),
            # Follow-up suggestions
            rx.cond(
                msg.suggestions.length() > 0,
                rx.vstack(
                    rx.text("Suggested follow-ups:",
                            font_size="0.7rem", color="#94A3B8",
                            font_weight="600", margin_top="10px"),
                    rx.box(
                        rx.foreach(msg.suggestions, _suggestion_chip),
                        flex_wrap="wrap", display="flex",
                    ),
                    spacing="0", align_items="start",
                ),
                rx.box(),
            ),
            spacing="0", align_items="start",
        ),
        spacing="3", align_items="flex-start",
    )


def _user_bubble(msg: Message) -> rx.Component:
    return rx.hstack(
        rx.box("U", width="28px", height="28px", border_radius="7px",
               flex_shrink="0", background="#F1F5F9",
               border="1px solid #E2E8F0", display="flex",
               align_items="center", justify_content="center",
               font_size="11px", font_weight="700", color="#64748B"),
        rx.box(
            rx.text(msg.content, font_size="0.875rem", color="white",
                    line_height="1.7"),
            padding="12px 16px", border_radius="12px 12px 3px 12px",
            background="linear-gradient(135deg, #2563EB, #4F46E5)",
            max_width="620px",
        ),
        spacing="3", align_items="flex-start",
        flex_direction="row-reverse",
    )


def chat_message(msg: Message) -> rx.Component:
    return rx.cond(msg.role == "user", _user_bubble(msg), _bot_bubble(msg))


def _chip(text: str) -> rx.Component:
    return rx.box(
        rx.text(text, font_size="0.8rem", color="#374151", font_weight="500"),
        padding="7px 14px", border_radius="8px",
        border="1.5px solid #E2E8F0", background="white",
        cursor="pointer", on_click=RAGState.set_user_input(text),
        _hover={"border_color": "#BFDBFE", "color": "#2563EB",
                "background": "#EFF6FF"},
        transition="all 0.18s ease",
    )


@rx.page(route="/chat", title="Chat — Nexus RAG")
def chat() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("Knowledge Chat", font_size="1.5rem",
                            font_weight="800", color="#0F172A",
                            letter_spacing="-0.025em", font_family=FONT),
                    rx.hstack(
                        rx.box(
                            width="7px", height="7px", border_radius="50%",
                            background=rx.cond(
                                RAGState.vectorstore_ready, "#22C55E", "#E2E8F0"
                            ),
                        ),
                        rx.text(
                            rx.cond(
                                RAGState.vectorstore_ready,
                                "Documents loaded — ready to answer",
                                "No documents — upload files first",
                            ),
                            font_size="0.82rem",
                            color=rx.cond(
                                RAGState.vectorstore_ready, "#15803D", "#94A3B8"
                            ),
                        ),
                        spacing="2", align_items="center",
                    ),
                    spacing="1", align_items="start",
                ),
                rx.hstack(
                    rx.cond(
                        ~RAGState.vectorstore_ready,
                        rx.link(
                            rx.box(
                                rx.text("Upload Documents",
                                        font_size="0.8rem", font_weight="600",
                                        color="#2563EB"),
                                padding="7px 16px", border_radius="8px",
                                background="#EFF6FF",
                                border="1.5px solid #BFDBFE", cursor="pointer",
                            ),
                            href="/upload",
                            _hover={"text_decoration": "none"},
                        ),
                        rx.box(),
                    ),
                    rx.box(
                        rx.text("Clear", font_size="0.8rem",
                                color="#94A3B8", font_weight="500"),
                        on_click=RAGState.clear_chat, cursor="pointer",
                        padding="7px 16px", border_radius="8px",
                        border="1.5px solid #E2E8F0", background="white",
                        _hover={"color": "#DC2626", "border_color": "#FECACA"},
                        transition="all 0.18s ease",
                    ),
                    spacing="2",
                ),
                justify="between", align_items="center",
                width="100%", margin_bottom="20px",
            ),

            # Chat window
            rx.box(
                rx.vstack(
                    rx.cond(
                        RAGState.messages.length() == 0,
                        rx.vstack(
                            rx.box(
                                rx.html('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'),
                                width="48px", height="48px", border_radius="12px",
                                background="linear-gradient(135deg, #2563EB, #4F46E5)",
                                display="flex", align_items="center",
                                justify_content="center",
                                box_shadow="0 4px 16px rgba(37,99,235,0.3)",
                            ),
                            rx.text("Ask your documents anything",
                                    font_size="1rem", font_weight="700",
                                    color="#0F172A", font_family=FONT),
                            rx.text(
                                rx.cond(
                                    RAGState.vectorstore_ready,
                                    "Documents loaded. Type a question or pick a suggestion below.",
                                    "Upload documents first, then return here to chat.",
                                ),
                                font_size="0.84rem", color="#94A3B8",
                                text_align="center",
                            ),
                            rx.hstack(
                                _chip("Summarise this document"),
                                _chip("What are the key findings?"),
                                _chip("List the main topics"),
                                spacing="2", flex_wrap="wrap", justify="center",
                            ),
                            spacing="4", align_items="center", padding="48px 24px",
                        ),
                        rx.box(),
                    ),
                    rx.foreach(RAGState.messages, chat_message),
                    # Typing indicator
                    rx.cond(
                        RAGState.is_loading,
                        rx.hstack(
                            rx.box(
                                rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>'),
                                width="28px", height="28px", border_radius="7px",
                                background="linear-gradient(135deg, #2563EB, #4F46E5)",
                                display="flex", align_items="center",
                                justify_content="center", flex_shrink="0",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.box(class_name="typing-dot"),
                                    rx.box(class_name="typing-dot"),
                                    rx.box(class_name="typing-dot"),
                                    class_name="typing-dots",
                                ),
                                rx.cond(
                                    RAGState.loading_status != "",
                                    rx.text(RAGState.loading_status,
                                            font_size="0.72rem",
                                            color="#94A3B8", margin_top="4px"),
                                    rx.box(),
                                ),
                                spacing="0", align_items="start",
                            ),
                            spacing="3", align_items="center",
                        ),
                        rx.box(),
                    ),
                    spacing="0", align_items="stretch",
                    width="100%", padding="20px", gap="18px",
                ),
                width="100%", border_radius="14px",
                background="#F8FAFC", border="1.5px solid #E2E8F0",
                overflow_y="auto", max_height="calc(100vh - 320px)",
                min_height="400px", margin_bottom="14px", flex="1",
            ),

            # Error
            rx.cond(
                RAGState.error_message != "",
                rx.box(
                    rx.text(RAGState.error_message, font_size="0.82rem"),
                    padding="11px 16px", border_radius="8px",
                    background="#FFF5F5", border="1px solid #FECACA",
                    color="#DC2626", margin_bottom="10px",
                ),
                rx.box(),
            ),

            # Input row
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="Ask a question about your documents...",
                        value=RAGState.user_input,
                        on_change=RAGState.set_user_input,
                        on_key_down=RAGState.send_on_enter,
                        disabled=RAGState.is_loading,
                        font_size="0.875rem", background="#F8FAFC",
                        color="#0F172A", border="1.5px solid #E2E8F0",
                        border_radius="9px", padding="12px 16px",
                        flex="1", height="46px",
                        _placeholder={"color": "#94A3B8"},
                        _focus={
                            "border_color": "#3B82F6", "outline": "none",
                            "box_shadow": "0 0 0 3px rgba(37,99,235,0.1)",
                            "background": "white",
                        },
                        _disabled={"opacity": "0.5", "cursor": "not-allowed"},
                        font_family=FONT,
                    ),
                    rx.box(
                        rx.cond(
                            RAGState.is_loading,
                            rx.html('<div style="width:16px;height:16px;border:2px solid rgba(255,255,255,0.4);border-top-color:white;border-radius:50%;animation:spin 0.75s linear infinite;"></div>'),
                            rx.html('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'),
                        ),
                        on_click=RAGState.send_message,
                        width="46px", height="46px", border_radius="9px",
                        background=rx.cond(
                            RAGState.is_loading | ~RAGState.vectorstore_ready,
                            "#E2E8F0",
                            "linear-gradient(135deg, #2563EB, #4F46E5)",
                        ),
                        display="flex", align_items="center",
                        justify_content="center",
                        cursor=rx.cond(
                            RAGState.is_loading | ~RAGState.vectorstore_ready,
                            "not-allowed", "pointer",
                        ),
                        box_shadow=rx.cond(
                            RAGState.is_loading | ~RAGState.vectorstore_ready,
                            "none", "0 2px 8px rgba(37,99,235,0.35)",
                        ),
                        transition="all 0.2s ease", flex_shrink="0",
                    ),
                    spacing="3", width="100%",
                ),
                padding="14px 16px", background="white",
                border="1.5px solid #E2E8F0", border_radius="12px",
                box_shadow="0 1px 4px rgba(0,0,0,0.06)",
            ),

            padding="84px 48px 40px", max_width="900px", margin="0 auto",
            min_height="calc(100vh - 60px)", display="flex",
            flex_direction="column",
        ),
        on_mount=[AuthState.require_auth, RAGState.set_active_page("chat"), RAGState.set_current_user(AuthState.user_id), RAGState.check_existing_index()],
        background="#F8FAFC", font_family=FONT,
    )
