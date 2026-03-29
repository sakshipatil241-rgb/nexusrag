import reflex as rx

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"

def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.text("N", font_size="0.75rem", font_weight="800",
                            color="white", font_family=FONT),
                    width="26px", height="26px", border_radius="6px",
                    background="linear-gradient(135deg, #2563EB, #4F46E5)",
                    display="flex", align_items="center", justify_content="center",
                ),
                rx.text("Nexus RAG", font_size="0.9rem", font_weight="700",
                        color="#475569", letter_spacing="-0.01em", font_family=FONT),
                spacing="2", align_items="center",
            ),
            rx.hstack(
                rx.link("Home",        href="/",        class_name="footer-link"),
                rx.link("Upload",      href="/upload",  class_name="footer-link"),
                rx.link("Chat",        href="/chat",    class_name="footer-link"),
                rx.link("History",     href="/history", class_name="footer-link"),
                rx.link("About",       href="/about",   class_name="footer-link"),
                rx.link("Groq API",    href="https://console.groq.com",
                        class_name="footer-link", is_external=True),
                rx.link("HuggingFace", href="https://huggingface.co",
                        class_name="footer-link", is_external=True),
                spacing="6", flex_wrap="wrap",
            ),
            rx.text("Built with Reflex · Groq · ChromaDB · LangChain",
                    font_size="0.75rem", color="#CBD5E1"),
            justify="between", align_items="center",
            width="100%", flex_wrap="wrap", gap="20px",
        ),
        class_name="nexus-footer",
    )
