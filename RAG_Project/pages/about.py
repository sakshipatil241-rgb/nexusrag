import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.rag_state import RAGState

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


def _what_card(icon_svg, title, desc):
    return rx.box(
        rx.box(rx.html(icon_svg), width="36px", height="36px",
               border_radius="9px", background="#EFF6FF",
               border="1px solid #BFDBFE", display="flex",
               align_items="center", justify_content="center",
               margin_bottom="14px"),
        rx.text(title, font_size="0.875rem", font_weight="700",
                color="#0F172A", margin_bottom="6px", font_family=FONT),
        rx.text(desc, font_size="0.8rem", color="#64748B", line_height="1.55"),
        padding="22px", border_radius="12px",
        background="white", border="1.5px solid #E2E8F0",
        _hover={"border_color": "#BFDBFE",
                "box_shadow": "0 4px 16px rgba(0,0,0,0.08)"},
        transition="all 0.2s ease",
    )


def _step_card(num, title, desc, color):
    return rx.box(
        rx.hstack(
            rx.box(rx.text(num, font_size="0.78rem", font_weight="800",
                          color="white"),
                   width="28px", height="28px", border_radius="50%",
                   background=color, display="flex",
                   align_items="center", justify_content="center",
                   flex_shrink="0"),
            rx.vstack(
                rx.text(title, font_size="0.875rem", font_weight="700",
                        color="#0F172A", font_family=FONT),
                rx.text(desc, font_size="0.8rem", color="#64748B",
                        line_height="1.5"),
                spacing="1", align_items="start",
            ),
            spacing="3", align_items="flex-start",
        ),
        padding="18px 20px", border_radius="10px",
        background="white", border="1.5px solid #E2E8F0",
    )


def _tech_card(icon_svg, name, role, color, bg):
    return rx.box(
        rx.hstack(
            rx.box(rx.html(icon_svg), width="40px", height="40px",
                   border_radius="10px", background=bg,
                   display="flex", align_items="center",
                   justify_content="center", flex_shrink="0"),
            rx.vstack(
                rx.text(name, font_size="0.875rem", font_weight="700",
                        color="#0F172A", font_family=FONT),
                rx.text(role, font_size="0.78rem", color="#64748B",
                        line_height="1.4"),
                spacing="0", align_items="start",
            ),
            spacing="3", align_items="center",
        ),
        padding="18px 20px", border_radius="10px",
        background="white", border="1.5px solid #E2E8F0",
        _hover={"border_color": "#BFDBFE",
                "box_shadow": "0 4px 12px rgba(0,0,0,0.08)"},
        transition="all 0.2s ease",
    )


def _qs_row(num, text):
    return rx.hstack(
        rx.box(rx.text(num, font_size="0.72rem", font_weight="700",
                      color="#2563EB"),
               width="24px", height="24px", border_radius="50%",
               background="#EFF6FF", border="1px solid #BFDBFE",
               display="flex", align_items="center",
               justify_content="center", flex_shrink="0"),
        rx.text(text, font_size="0.875rem", color="#374151",
                line_height="1.5"),
        spacing="3", align_items="center",
    )


@rx.page(route="/about", title="About — Nexus RAG")
def about() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            # Hero
            rx.vstack(
                rx.box(rx.text("AI DOCUMENT INTELLIGENCE", font_size="0.68rem",
                               font_weight="700", color="#2563EB",
                               letter_spacing="0.1em"),
                       padding="4px 12px", border_radius="20px",
                       background="#EFF6FF", border="1px solid #BFDBFE",
                       display="inline-block", margin_bottom="16px"),
                rx.text("About Nexus RAG", font_size="2.2rem",
                        font_weight="800", color="#0F172A",
                        letter_spacing="-0.03em", font_family=FONT),
                rx.text(
                    "An AI-powered document search assistant that answers "
                    "questions strictly from your uploaded documents — "
                    "with source attribution on every response.",
                    font_size="1rem", color="#64748B", line_height="1.75",
                    max_width="580px",
                ),
                spacing="3", align_items="start", margin_bottom="48px",
            ),

            rx.vstack(
                # What it does
                rx.box(
                    rx.text("What it does", font_size="0.68rem",
                            font_weight="700", color="#64748B",
                            letter_spacing="0.1em", margin_bottom="16px"),
                    rx.grid(
                        _what_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
                                   "Upload Documents",
                                   "Ingest PDF, TXT, and CSV files. Documents are split into segments and indexed automatically."),
                        _what_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
                                   "Semantic Search",
                                   "Queries matched by meaning, not keywords, using vector similarity across your content."),
                        _what_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
                                   "Cited Answers",
                                   "Every response is grounded in your documents with source file attribution."),
                        _what_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.79"/></svg>',
                                   "Self-Correcting",
                                   "Detects poor retrievals and rewrites queries automatically to improve accuracy."),
                        columns="4", spacing="4", width="100%",
                    ),
                    width="100%",
                ),

                # How it works
                rx.box(
                    rx.text("How it works", font_size="0.68rem",
                            font_weight="700", color="#64748B",
                            letter_spacing="0.1em", margin_bottom="16px"),
                    rx.vstack(
                        _step_card("1", "Upload & Index",
                                   "Documents chunked into 800-character segments and converted to vector embeddings stored in ChromaDB.",
                                   "#2563EB"),
                        _step_card("2", "Query & Retrieve",
                                   "Your question is embedded and matched against the index using MMR retrieval for diverse, relevant results.",
                                   "#4F46E5"),
                        _step_card("3", "Evaluate & Correct",
                                   "LLM checks if retrieved content is relevant. If not, the query is rewritten and retrieval runs again.",
                                   "#7C3AED"),
                        _step_card("4", "Generate & Cite",
                                   "Groq LLaMA 3.1 synthesises a precise answer from the verified context with source attribution.",
                                   "#059669"),
                        spacing="3", width="100%",
                    ),
                    width="100%",
                ),

                # Tech stack
                rx.box(
                    rx.text("Technology", font_size="0.68rem",
                            font_weight="700", color="#64748B",
                            letter_spacing="0.1em", margin_bottom="16px"),
                    rx.grid(
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="1.8"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
                                   "Reflex", "Python full-stack framework", "#4F46E5", "#EEF2FF"),
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="1.8"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
                                   "LangChain", "RAG orchestration", "#059669", "#ECFDF5"),
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="1.8"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
                                   "Groq + LLaMA 3.1", "Sub-second inference", "#D97706", "#FFFBEB"),
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
                                   "HuggingFace MiniLM", "Sentence embeddings", "#2563EB", "#EFF6FF"),
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="1.8"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
                                   "ChromaDB", "Local vector database", "#7C3AED", "#F5F3FF"),
                        _tech_card('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
                                   "PDF / TXT / CSV", "Multi-format ingestion", "#DC2626", "#FFF5F5"),
                        columns="3", spacing="4", width="100%",
                    ),
                    width="100%",
                ),

                # Quick start
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Get started in 3 steps",
                                    font_size="1.1rem", font_weight="800",
                                    color="#0F172A", font_family=FONT),
                            rx.text(
                                "Upload your documents and start asking questions.",
                                font_size="0.875rem", color="#64748B",
                                line_height="1.6", max_width="380px",
                            ),
                            rx.hstack(
                                rx.link(
                                    rx.box(
                                        rx.text("Upload Documents",
                                                font_size="0.84rem",
                                                font_weight="600",
                                                color="white"),
                                        padding="10px 22px",
                                        border_radius="8px",
                                        background="linear-gradient(135deg, #2563EB, #4F46E5)",
                                        cursor="pointer",
                                    ),
                                    href="/upload",
                                    _hover={"text_decoration": "none"},
                                ),
                                rx.link(
                                    rx.box(
                                        rx.text("Start Chat",
                                                font_size="0.84rem",
                                                font_weight="500",
                                                color="#2563EB"),
                                        padding="10px 22px",
                                        border_radius="8px",
                                        background="#EFF6FF",
                                        border="1.5px solid #BFDBFE",
                                        cursor="pointer",
                                    ),
                                    href="/chat",
                                    _hover={"text_decoration": "none"},
                                ),
                                spacing="3",
                            ),
                            spacing="4", align_items="start",
                        ),
                        rx.vstack(
                            _qs_row("1", "Upload PDF, TXT, or CSV on the Upload page"),
                            _qs_row("2", "Wait for indexing to complete"),
                            _qs_row("3", "Open Chat and ask questions"),
                            spacing="3", align_items="start", flex="1",
                        ),
                        spacing="9", align_items="center",
                        flex_wrap="wrap", gap="32px",
                    ),
                    padding="36px 40px", border_radius="16px",
                    background="white", border="1.5px solid #E2E8F0",
                    box_shadow="0 2px 8px rgba(0,0,0,0.05)",
                ),

                spacing="8", align_items="start", width="100%",
            ),

            class_name="page-content",
        ),
        footer(),
        on_mount=[RAGState.set_active_page("about"),
                  RAGState.check_existing_index()],
        background="#F8FAFC", min_height="100vh", font_family=FONT,
    )
