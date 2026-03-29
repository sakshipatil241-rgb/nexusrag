import reflex as rx
from RAG_Project.states.auth_state import AuthState

FONT = "'Plus Jakarta Sans', 'Inter', sans-serif"


@rx.page(route="/login", title="Sign In — Nexus RAG")
def login() -> rx.Component:
    return rx.box(
        # Background
        rx.box(
            position="fixed", inset="0",
            background="linear-gradient(135deg, #EFF6FF 0%, #F0F4FF 50%, #EEF2FF 100%)",
            z_index="-1",
        ),

        rx.box(
            # Logo
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.text("N", font_size="1rem", font_weight="800",
                                color="white", font_family=FONT),
                        width="38px", height="38px", border_radius="10px",
                        background="linear-gradient(135deg, #2563EB, #4F46E5)",
                        display="flex", align_items="center",
                        justify_content="center",
                        box_shadow="0 2px 10px rgba(37,99,235,0.35)",
                    ),
                    rx.vstack(
                        rx.text("Nexus RAG", font_size="1rem", font_weight="800",
                                color="#0F172A", letter_spacing="-0.02em",
                                font_family=FONT),
                        rx.text("AI Document Search", font_size="0.7rem",
                                color="#64748B"),
                        spacing="0", align_items="start",
                    ),
                    spacing="3", align_items="center",
                ),
                href="/", _hover={"text_decoration": "none"},
            ),
            display="flex", justify_content="center",
            padding="32px 0 0",
        ),

        # Card
        rx.box(
            rx.vstack(
                rx.text("Welcome back", font_size="1.6rem", font_weight="800",
                        color="#0F172A", letter_spacing="-0.025em",
                        font_family=FONT, text_align="center"),
                rx.text("Sign in to your account to continue",
                        font_size="0.875rem", color="#64748B",
                        text_align="center"),
                spacing="2", margin_bottom="28px", align_items="center",
            ),

            # Error
            rx.cond(
                AuthState.login_error != "",
                rx.box(
                    rx.hstack(
                        rx.html('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'),
                        rx.text(AuthState.login_error, font_size="0.84rem"),
                        spacing="2", align_items="center",
                    ),
                    padding="10px 14px", border_radius="8px",
                    background="#FFF5F5", border="1px solid #FECACA",
                    color="#DC2626", margin_bottom="16px",
                ),
                rx.box(),
            ),

            # Form
            rx.vstack(
                rx.vstack(
                    rx.text("Username", font_size="0.82rem", font_weight="600",
                            color="#374151"),
                    rx.input(
                        placeholder="Enter your username",
                        value=AuthState.login_username,
                        on_change=AuthState.set_login_username,
                        on_key_down=AuthState.do_login_enter,
                        font_size="0.875rem", border="1.5px solid #E2E8F0",
                        border_radius="9px", padding="11px 14px",
                        background="white", color="#0F172A",
                        width="100%",
                        _focus={"border_color": "#3B82F6", "outline": "none",
                                "box_shadow": "0 0 0 3px rgba(37,99,235,0.1)"},
                        _placeholder={"color": "#94A3B8"},
                        font_family=FONT,
                    ),
                    spacing="2", align_items="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Password", font_size="0.82rem", font_weight="600",
                            color="#374151"),
                    rx.input(
                        placeholder="Enter your password",
                        value=AuthState.login_password,
                        on_change=AuthState.set_login_password,
                        on_key_down=AuthState.do_login_enter,
                        type="password",
                        font_size="0.875rem", border="1.5px solid #E2E8F0",
                        border_radius="9px", padding="11px 14px",
                        background="white", color="#0F172A",
                        width="100%",
                        _focus={"border_color": "#3B82F6", "outline": "none",
                                "box_shadow": "0 0 0 3px rgba(37,99,235,0.1)"},
                        _placeholder={"color": "#94A3B8"},
                        font_family=FONT,
                    ),
                    spacing="2", align_items="start", width="100%",
                ),
                rx.box(
                    rx.cond(
                        AuthState.is_loading,
                        rx.hstack(
                            rx.html('<div style="width:14px;height:14px;border:2px solid rgba(255,255,255,0.4);border-top-color:white;border-radius:50%;animation:spin 0.75s linear infinite;"></div>'),
                            rx.text("Signing in...", font_size="0.875rem",
                                    font_weight="600", color="white"),
                            spacing="2", align_items="center",
                        ),
                        rx.text("Sign In", font_size="0.875rem",
                                font_weight="600", color="white"),
                    ),
                    on_click=AuthState.do_login,
                    width="100%", padding="12px",
                    border_radius="9px", cursor="pointer",
                    background="linear-gradient(135deg, #2563EB, #4F46E5)",
                    box_shadow="0 2px 10px rgba(37,99,235,0.35)",
                    display="flex", align_items="center",
                    justify_content="center",
                    _hover={"box_shadow": "0 4px 16px rgba(37,99,235,0.45)",
                            "transform": "translateY(-1px)"},
                    transition="all 0.2s ease",
                ),
                spacing="4", width="100%",
            ),

            rx.hstack(
                rx.box(height="1px", background="#E2E8F0", flex="1"),
                rx.text("or", font_size="0.78rem", color="#94A3B8",
                        padding="0 12px"),
                rx.box(height="1px", background="#E2E8F0", flex="1"),
                align_items="center", width="100%", margin="20px 0",
            ),

            rx.box(
                rx.hstack(
                    rx.text("Don't have an account?",
                            font_size="0.84rem", color="#64748B"),
                    rx.link(
                        rx.text("Create account", font_size="0.84rem",
                                font_weight="600", color="#2563EB"),
                        href="/register",
                        _hover={"text_decoration": "none",
                                "color": "#1D4ED8"},
                    ),
                    spacing="2", justify="center",
                ),
                text_align="center",
            ),

            background="white", border_radius="16px",
            border="1.5px solid #E2E8F0",
            box_shadow="0 8px 32px rgba(0,0,0,0.08)",
            padding="40px",
            width="420px",
            margin="40px auto 0",
        ),

        min_height="100vh", font_family=FONT,
        on_mount=AuthState.clear_errors,
    )
