import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Google Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_AGENT_MODEL = os.getenv("GOOGLE_AGENT_MODEL")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_AGENT_MODEL = os.getenv("OPENAI_AGENT_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

# Provider Configuration
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "google").lower()

# Database Configuration
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")

# File Paths
raw_pdf_path = os.getenv("PDF_PATH")
PDF_PATH = Path(raw_pdf_path) if raw_pdf_path else None
raw_prompt_path = os.getenv("PROMPT_PATH")
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "search_prompt.txt"