from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from config import get_chat_model
from config.constants import PROMPT_PATH
from config.database import get_doc_storage

def search_prompt(provider: str = None):
    """
    Create a prompt template for the search from a text file.
    
    Args:
        provider: Optional provider name ("openai" or "google").
                 If not provided, uses EMBEDDING_PROVIDER from config.
    
    Returns:
        PromptTemplate: configured prompt template.
    """
    if not PROMPT_PATH or not PROMPT_PATH.exists():
        raise FileNotFoundError(f"O arquivo de prompt não foi encontrado em '{PROMPT_PATH}'")

    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    question_template = PromptTemplate(
        template=prompt_template,
        input_variables=["contexto", "pergunta"],
    )

    model = get_chat_model(provider)
    return question_template | model

def search_results(question: str, provider: str = None):
    """
    Search for results in the document storage.
    
    Args:
        question: The question to search for.
        provider: Optional provider name ("openai" or "google").
                 If not provided, uses EMBEDDING_PROVIDER from config.
    
    Returns:
        list: The list of results.
    """
    doc_storage = get_doc_storage(provider)
    return doc_storage.similarity_search_with_score(question, k=10)