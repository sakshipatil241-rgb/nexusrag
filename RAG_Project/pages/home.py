import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.rag_state  import RAGState
from RAG_Project.states.auth_state import AuthState

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


def hero_section() -> rx.Component:
    return rx.box(
        rx.box(

            # Headline
            rx.box(
                rx.text("AI-Powered Document Search &",
                        font_size="clamp(2.2rem, 4.5vw, 3.8rem)",
                        font_weight="800", color="#0F172A",
                        letter_spacing="-0.035em", line_height="1.1",
                        font_family=FONT),
                rx.html(
                    '<span class="grad-text" style="'
                    'font-family:Plus Jakarta Sans,Inter,sans-serif;'
                    'font-size:clamp(2.2rem,4.5vw,3.8rem);'
                    'font-weight:800;letter-spacing:-0.035em;line-height:1.1;'
                    'display:block;">Knowledge Assistant</span>'
                ),
                margin_bottom="24px", class_name="hero-anim-2",
            ),
            # Subtitle
            rx.text(
                "Upload your documents. Ask anything in natural language. "
                "Get precise, cited answers powered by retrieval-augmented generation.",
                font_size="1.05rem", color="#475569", line_height="1.75",
                max_width="540px", text_align="center", margin_bottom="40px",
                class_name="hero-anim-3", font_family=FONT,
            ),
            # CTAs
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.html('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'),
                        rx.text("Start Chat", font_weight="600"),
                        spacing="2", align_items="center",
                    ),
                    href=rx.cond(AuthState.is_logged_in, "/chat", "/login"),
                    class_name="btn-primary",
                    _hover={"text_decoration": "none"},
                ),
                rx.link(
                    rx.hstack(
                        rx.html('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>'),
                        rx.text(rx.cond(AuthState.is_logged_in, "Upload Documents", "Create Account"), font_weight="500"),
                        spacing="2", align_items="center",
                    ),
                    href=rx.cond(AuthState.is_logged_in, "/upload", "/register"),
                    class_name="btn-ghost",
                    _hover={"text_decoration": "none"},
                ),
                spacing="4", justify="center", flex_wrap="wrap",
                class_name="hero-anim-4", margin_bottom="64px",
            ),

            display="flex", flex_direction="column", align_items="center",
            text_align="center", max_width="900px", margin="0 auto",
        ),
        class_name="hero-section",
        padding="120px 48px 80px",
        position="relative",
    )


def _stat(val, label):
    return rx.vstack(
        rx.text(val, font_size="1rem", font_weight="800",
                color="#0F172A", letter_spacing="-0.02em", font_family=FONT),
        rx.text(label, font_size="0.72rem", color="#94A3B8"),
        spacing="1", align_items="center",
    )


def _feat(icon_svg, title, desc):
    return rx.box(
        rx.box(rx.html(icon_svg), class_name="feat-icon-wrap"),
        rx.text(title, font_size="0.95rem", font_weight="700",
                color="#0F172A", margin_bottom="8px", font_family=FONT),
        rx.text(desc, font_size="0.84rem", color="#64748B", line_height="1.6"),
        class_name="feat-card",
    )


def features_section() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("Platform Capabilities", class_name="sec-eyebrow"),
            rx.text("Everything you need for intelligent document search", class_name="sec-title"),
            rx.text("From ingestion to citation — a complete pipeline built for accuracy, speed, and traceability.", class_name="sec-sub"),
            rx.grid(
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
                      "Semantic Search", "Understands query intent far beyond keyword matching — finds conceptually related content across all documents."),
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                      "Source Attribution", "Every answer cites the exact source documents — so you know precisely where each fact comes from."),
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.79"/></svg>',
                      "Self-Correcting RAG", "Detects poor retrievals, rewrites the query automatically, and re-retrieves for consistently accurate answers."),
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
                      "Conversational Memory", "Full session context preserved — enabling natural follow-ups and multi-step discovery."),
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 3v18"/></svg>',
                      "Multi-Format Ingestion", "Ingest PDF, TXT, and CSV files through a unified pipeline — chunked, cleaned, and indexed instantly."),
                _feat('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
                      "Groq-Powered Speed", "LLaMA 3.1 8B on Groq's LPU hardware — sub-second inference, fastest open-source LLM runtime."),
                columns="3", spacing="4", width="100%",
            ),
            max_width="1100px", margin="0 auto",
        ),
        padding="80px 48px", background="white",
        border_top="1px solid #E2E8F0",
    )


def _pipe_node(icon_svg, label, border_color, bg_color, tooltip):
    return rx.vstack(
        rx.box(
            rx.html(icon_svg),
            rx.box(rx.text(tooltip, font_size="0.7rem", color="white",
                           line_height="1.5", text_align="center"),
                   class_name="pipeline-tooltip"),
            class_name="pipeline-node-circle",
            style={"background": bg_color, "border_color": border_color},
        ),
        rx.text(label, font_size="0.68rem", font_weight="600", color="#64748B",
                text_align="center", line_height="1.3", font_family=FONT),
        spacing="3", align_items="center", width="96px",
    )


def _pipe_arrow():
    return rx.html(
        '<svg width="44" height="14" viewBox="0 0 44 14" style="flex-shrink:0">'
        '<path class="flow-arrow-path" d="M2 7 H36" stroke="#CBD5E1" stroke-width="1.5" fill="none"/>'
        '<polygon points="32,3 40,7 32,11" fill="#CBD5E1"/>'
        '</svg>'
    )


def pipeline_section() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("How It Works", class_name="sec-eyebrow"),
            rx.text("The Corrective RAG Pipeline", class_name="sec-title"),
            rx.text("Six stages from document upload to cited answer — automatic quality control at every step. Hover each node for details.", class_name="sec-sub"),
            rx.box(
                rx.hstack(
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
                               "Ingestion", "#BFDBFE", "#EFF6FF", "Upload PDF, TXT, CSV. Files are chunked and cleaned for processing."),
                    _pipe_arrow(),
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
                               "Embedding", "#C7D2FE", "#EEF2FF", "HuggingFace all-MiniLM-L6-v2 encodes chunks into high-dimensional vectors."),
                    _pipe_arrow(),
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
                               "Retrieval", "#DDD6FE", "#F5F3FF", "MMR retrieves top-k semantically diverse and relevant chunks."),
                    _pipe_arrow(),
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
                               "Evaluation", "#FDE68A", "#FFFBEB", "LLM evaluates relevance: YES → synthesize, NO → rewrite query."),
                    _pipe_arrow(),
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
                               "Synthesis", "#A7F3D0", "#ECFDF5", "Groq LLaMA 3.1 synthesizes a coherent answer from verified context."),
                    _pipe_arrow(),
                    _pipe_node('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
                               "Response", "#BFDBFE", "#EFF6FF", "Final answer returned with cited source documents for full traceability."),
                    spacing="0", align_items="center", justify="center",
                    width="100%", flex_wrap="wrap", gap="6px",
                ),
                padding="40px 28px",
                class_name="pipeline-wrap",
                margin_bottom="16px",
            ),
            rx.hstack(
                rx.html('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="1.8"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.79"/></svg>'),
                rx.text("Correction loop: if relevance check fails, the query is rewritten and re-retrieved automatically before synthesis.",
                        font_size="0.8rem", color="#92400E"),
                spacing="3", align_items="center",
                padding="12px 20px", border_radius="9px",
                background="#FFFBEB", border="1px solid #FDE68A",
            ),
            max_width="1100px", margin="0 auto",
        ),
        padding="80px 48px", background="#F8FAFC",
        border_top="1px solid #E2E8F0",
    )


def chat_preview_section() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("Live Interface", class_name="sec-eyebrow"),
            rx.text("See it in action", class_name="sec-title"),
            rx.text("A natural language interface that understands your documents and delivers precise, cited answers instantly.", class_name="sec-sub"),
            rx.box(
                rx.hstack(
                    rx.box(rx.html('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'), class_name="chat-avatar-icon"),
                    rx.vstack(
                        rx.text("Nexus RAG Assistant", font_size="0.88rem", font_weight="700", color="#0F172A", font_family=FONT),
                        rx.hstack(rx.box(class_name="chat-online-dot"),
                                  rx.text("Online · 3 documents indexed", font_size="0.72rem", color="#64748B"),
                                  spacing="2", align_items="center"),
                        spacing="0", align_items="start",
                    ),
                    spacing="3", align_items="center", class_name="chat-header-bar",
                ),
                rx.box(
                    rx.hstack(
                        rx.box(rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>'), class_name="bot-avatar-sm"),
                        rx.box(rx.text("Hello! I'm Nexus RAG. I've indexed your documents and I'm ready to answer questions.", font_size="0.875rem", line_height="1.65"), class_name="bot-bubble"),
                        spacing="3", align_items="flex-start", class_name="chat-msg-bot",
                    ),
                    rx.hstack(
                        rx.box("U", class_name="user-avatar-sm"),
                        rx.box(rx.text("What are the main topics covered in the documents?", font_size="0.875rem", line_height="1.65"), class_name="user-bubble"),
                        spacing="3", align_items="flex-start", class_name="chat-msg-user",
                    ),
                    rx.hstack(
                        rx.box(rx.html('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>'), class_name="bot-avatar-sm"),
                        rx.box(rx.box(class_name="typing-dot"), rx.box(class_name="typing-dot"), rx.box(class_name="typing-dot"), class_name="typing-dots"),
                        spacing="3", align_items="center", class_name="chat-msg-bot",
                    ),
                    class_name="chat-messages-area", gap="16px",
                ),
                rx.hstack(
                    rx.html('<input class="nexus-chat-input" type="text" placeholder="Ask a question about your documents…" disabled/>'),
                    rx.box(rx.html('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'), class_name="chat-send-btn"),
                    spacing="3", align_items="center", class_name="chat-input-zone",
                ),
                class_name="chat-wrap",
            ),
            max_width="800px", margin="0 auto",
        ),
        padding="80px 48px", background="white", border_top="1px solid #E2E8F0",
    )


@rx.page(route="/", title="Nexus RAG — AI Document Intelligence")
def home() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            hero_section(),
            rx.html('<hr class="divider-line"/>'),
            features_section(),
            rx.html('<hr class="divider-line"/>'),
            pipeline_section(),
            rx.html('<hr class="divider-line"/>'),
            chat_preview_section(),
            rx.html('<hr class="divider-line"/>'),
            footer(),
        ),
        on_mount=[RAGState.set_active_page("home")],
        background="#F8FAFC", min_height="100vh", font_family=FONT,
    )
