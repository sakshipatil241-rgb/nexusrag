import reflex as rx
from RAG_Project.components.navbar import navbar
from RAG_Project.components.footer import footer
from RAG_Project.states.rag_state  import RAGState
from RAG_Project.states.auth_state import AuthState
from RAG_Project.states.rag_state  import RAGState, DocStat

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


def _step(num: str, text: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(num, font_size="0.7rem", font_weight="700", color="#2563EB"),
            width="22px", height="22px", border_radius="50%",
            background="#EFF6FF", border="1px solid #BFDBFE",
            display="flex", align_items="center", justify_content="center",
            flex_shrink="0",
        ),
        rx.text(text, font_size="0.82rem", color="#64748B", line_height="1.4"),
        spacing="3", align_items="center",
    )


def doc_stat_card(ds: DocStat) -> rx.Component:
    """Card for each uploaded document with stats + summary."""
    return rx.box(
        # File name + size
        rx.hstack(
            rx.html('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>'),
            rx.html('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
            rx.text(ds.filename, font_size="0.84rem", font_weight="600",
                    color="#0F172A", flex="1"),
            rx.text(
                rx.cond(ds.size_kb > 0, f"{ds.size_kb} KB", ""),
                font_size="0.72rem", color="#94A3B8",
            ),
            rx.cond(
                ds.chunks > 0,
                rx.box(
                    rx.text(f"{ds.chunks} segments", font_size="0.68rem",
                            color="#2563EB", font_weight="600"),
                    padding="2px 7px", border_radius="4px",
                    background="#EFF6FF", border="1px solid #BFDBFE",
                ),
                rx.box(),
            ),
            spacing="2", align_items="center", width="100%",
        ),
        # Summary section
        rx.cond(
            ds.summary != "",
            rx.box(
                rx.text(ds.summary, font_size="0.8rem", color="#64748B",
                        line_height="1.55", margin_top="8px",
                        font_style=rx.cond(
                            ds.summarising, "italic", "normal"
                        )),
            ),
            rx.box(),
        ),
        # Summarise button
        rx.cond(
            ~ds.summarising & (ds.summary == ""),
            rx.box(
                rx.hstack(
                    rx.html('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'),
                    rx.text("Generate summary", font_size="0.72rem",
                            font_weight="500"),
                    spacing="1", align_items="center",
                ),
                margin_top="8px", padding="4px 10px", border_radius="5px",
                background="#F8FAFC", border="1px solid #E2E8F0",
                cursor="pointer", color="#64748B",
                display="inline-flex",
                on_click=RAGState.summarise_doc(ds.filename),
                _hover={"background": "#EFF6FF", "color": "#2563EB",
                        "border_color": "#BFDBFE"},
                transition="all 0.15s ease",
            ),
            rx.box(),
        ),
        padding="12px 16px",
        border_bottom="1px solid #F1F5F9",
        width="100%",
    )


@rx.page(route="/upload", title="Upload — Nexus RAG")
def upload() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.text("Document Upload", font_size="1.75rem",
                        font_weight="800", color="#0F172A",
                        letter_spacing="-0.025em", font_family=FONT),
                rx.text(
                    "Upload PDF, TXT, or CSV files. Documents are chunked, "
                    "embedded, and indexed for semantic search.",
                    font_size="0.9rem", color="#64748B", line_height="1.7",
                    max_width="540px",
                ),
                spacing="3", align_items="start", margin_bottom="36px",
            ),

            rx.grid(
                # Left — upload controls
                rx.vstack(
                    rx.upload(
                        rx.box(
                            rx.html('<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>'),
                            rx.text("Drop files here or click to browse",
                                    font_size="0.9rem", font_weight="600",
                                    color="#64748B", margin_top="16px"),
                            rx.text("Supports PDF · TXT · CSV",
                                    font_size="0.78rem", color="#94A3B8",
                                    margin_top="6px"),
                            display="flex", flex_direction="column",
                            align_items="center", justify_content="center",
                            padding="60px 32px",
                        ),
                        id="doc_upload",
                        accept={
                            "application/pdf": [".pdf"],
                            "text/plain": [".txt"],
                            "text/csv": [".csv"],
                        },
                        multiple=True,
                        class_name="upload-dropzone",
                        width="100%",
                    ),

                    # Selected files preview
                    rx.cond(
                        rx.selected_files("doc_upload") != [],
                        rx.box(
                            rx.text("SELECTED FILES", font_size="0.65rem",
                                    font_weight="700", color="#94A3B8",
                                    letter_spacing="0.1em", margin_bottom="10px"),
                            rx.vstack(
                                rx.foreach(
                                    rx.selected_files("doc_upload"),
                                    lambda f: rx.hstack(
                                        rx.html('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'),
                                        rx.text(f, font_size="0.84rem",
                                                color="#475569"),
                                        spacing="2", align_items="center",
                                    ),
                                ),
                                spacing="2", align_items="start",
                            ),
                            class_name="upload-card", width="100%",
                        ),
                        rx.box(),
                    ),

                    # Upload button
                    rx.box(
                        rx.cond(
                            RAGState.is_uploading,
                            rx.hstack(
                                rx.box(class_name="spinner"),
                                rx.text("Processing...", font_size="0.9rem",
                                        font_weight="600", color="white"),
                                spacing="2", align_items="center",
                            ),
                            rx.hstack(
                                rx.html('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>'),
                                rx.text("Upload & Index Documents",
                                        font_size="0.9rem", font_weight="600"),
                                spacing="2", align_items="center",
                            ),
                        ),
                        on_click=RAGState.handle_upload(
                            rx.upload_files(upload_id="doc_upload")
                        ),
                        padding="12px 28px", border_radius="9px",
                        background=rx.cond(
                            RAGState.is_uploading, "#94A3B8",
                            "linear-gradient(135deg, #2563EB, #4F46E5)"
                        ),
                        color="white",
                        cursor=rx.cond(RAGState.is_uploading,
                                       "not-allowed", "pointer"),
                        display="inline-flex", align_items="center",
                        box_shadow=rx.cond(
                            RAGState.is_uploading, "none",
                            "0 2px 10px rgba(37,99,235,0.35)"
                        ),
                        transition="all 0.2s", font_family=FONT,
                    ),

                    # Status
                    rx.cond(
                        RAGState.upload_status != "",
                        rx.box(
                            rx.text(RAGState.upload_status, font_size="0.84rem"),
                            class_name=rx.cond(
                                RAGState.upload_status.contains("processed")
                                | RAGState.upload_status.contains("processed"),
                                "status-success",
                                rx.cond(
                                    RAGState.upload_status.contains("Failed")
                                    | RAGState.upload_status.contains("failed"),
                                    "status-error",
                                    "status-info",
                                ),
                            ),
                            width="100%",
                        ),
                        rx.box(),
                    ),

                    spacing="4", align_items="start", width="100%",
                ),

                # Right — status + doc stats + clear
                rx.vstack(
                    # Status indicator
                    rx.box(
                        rx.hstack(
                            rx.box(
                                width="10px", height="10px",
                                border_radius="50%",
                                background=rx.cond(
                                    RAGState.vectorstore_ready, "#22C55E", "#E2E8F0"
                                ),
                            ),
                            rx.text(
                                rx.cond(
                                    RAGState.vectorstore_ready,
                                    "Documents loaded — go to Chat to search",
                                    "No documents — upload files to begin",
                                ),
                                font_size="0.84rem", font_weight="600",
                                color=rx.cond(
                                    RAGState.vectorstore_ready, "#15803D", "#64748B"
                                ),
                            ),
                            spacing="2", align_items="center",
                        ),
                        padding="14px 18px", border_radius="9px",
                        background=rx.cond(
                            RAGState.vectorstore_ready, "#F0FDF4", "#F8FAFC"
                        ),
                        border=rx.cond(
                            RAGState.vectorstore_ready,
                            "1px solid #BBF7D0", "1px solid #E2E8F0"
                        ),
                        width="100%",
                    ),

                    # Document stats cards
                    rx.cond(
                        RAGState.doc_stats.length() > 0,
                        rx.box(
                            rx.hstack(
                                rx.text("DOCUMENTS", font_size="0.65rem",
                                        font_weight="700", color="#94A3B8",
                                        letter_spacing="0.1em"),
                                rx.link(
                                    rx.text("Open Chat →", font_size="0.8rem",
                                            color="#2563EB", font_weight="600"),
                                    href="/chat",
                                    _hover={"text_decoration": "none",
                                            "color": "#1D4ED8"},
                                ),
                                justify="between", width="100%",
                                margin_bottom="8px",
                            ),
                            rx.vstack(
                                rx.foreach(RAGState.doc_stats, doc_stat_card),
                                spacing="0", width="100%",
                            ),
                            class_name="upload-card", width="100%",
                            padding="14px 16px",
                        ),
                        rx.box(),
                    ),

                    # Clear all documents button
                    rx.cond(
                        RAGState.doc_stats.length() > 0,
                        rx.box(
                            rx.hstack(
                                rx.html('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'),
                                rx.text("Delete all documents",
                                        font_size="0.8rem", font_weight="500"),
                                spacing="2", align_items="center",
                            ),
                            on_click=RAGState.delete_all_documents,
                            cursor="pointer", padding="8px 16px",
                            border_radius="8px", border="1.5px solid #E2E8F0",
                            background="white", color="#94A3B8",
                            display="inline-flex",
                            _hover={"color": "#DC2626",
                                    "border_color": "#FECACA",
                                    "background": "#FFF5F5"},
                            transition="all 0.18s ease",
                        ),
                        rx.box(),
                    ),

                    # How to use
                    rx.box(
                        rx.text("How to use", font_size="0.78rem",
                                font_weight="700", color="#374151",
                                margin_bottom="12px"),
                        rx.vstack(
                            _step("1", "Select PDF, TXT, or CSV files"),
                            _step("2", "Click Upload & Index Documents"),
                            _step("3", "Click 'Generate summary' on any file"),
                            _step("4", "Go to Chat and ask questions"),
                            spacing="3", align_items="start",
                        ),
                        padding="18px 20px", border_radius="10px",
                        background="#F8FAFC", border="1px solid #E2E8F0",
                        width="100%",
                    ),

                    spacing="4", align_items="start", width="100%",
                ),

                columns="2", spacing="6", width="100%",
            ),

            class_name="page-content",
        ),
        footer(),
        on_mount=[AuthState.require_auth, RAGState.set_active_page("upload"), RAGState.set_current_user(AuthState.user_id), RAGState.check_existing_index()],
        background="#F8FAFC", min_height="100vh", font_family=FONT,
    )
