import reflex as rx
import os

config = rx.Config(
    app_name="RAG_Project",
    plugins=[
        rx.plugins.SitemapPlugin(),
    ],
    env={
        "GROQ_API_KEY":os.getenv("GROQ_API_KEY"),
        "HUGGINGFACEHUB_API_TOKEN":os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    }
)