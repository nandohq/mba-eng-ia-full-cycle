"""
Main source package for the application.

This package provides document ingestion, search, and chat functionality
using LangChain and PostgreSQL with pgvector.
"""

from .ingest import ingest_pdf
from .search import search_prompt

__all__ = [
    "ingest_pdf",
    "search_prompt",
]

