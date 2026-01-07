import os

from pathlib import Path
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from .validation import validate_provider, validate_env_vars

from .constants import (
    OPENAI_API_KEY,
    OPENAI_AGENT_MODEL,
    OPENAI_EMBEDDING_MODEL,
    GOOGLE_API_KEY,
    GOOGLE_AGENT_MODEL,
    GOOGLE_EMBEDDING_MODEL
)

def get_agent_model(provider: str = None) -> str:
    """
    Get the agent model based on the provider.

    Args:
        provider: Optional provider name. Can be "openai" or "google".
                 If not provided, uses EMBEDDING_PROVIDER from config.
    
    Returns:
        str: the agent model name.
    
    Raises:
        SystemExit: If the provider is not supported, display a friendly message and exit.
    """
    normalized_provider = validate_provider(provider)
    
    if normalized_provider == "openai":
        return OPENAI_AGENT_MODEL
        
    return GOOGLE_AGENT_MODEL

def get_chat_model(provider: str = None) -> BaseChatModel:
    """
    Create a chat model instance based on the configured provider.
    
    Args:
        provider: Optional provider name. Can be "openai" or "google". 
                 If not provided, uses EMBEDDING_PROVIDER from config.
    
    Returns:
        BaseChatModel: configured chat model instance (OpenAI or Google).
    
    Raises:
        SystemExit: If the provider is not supported, display a friendly message and exit.
    """
    normalized_provider = validate_provider(provider)
    
    if normalized_provider == "openai":
        validate_env_vars("OPENAI_API_KEY", "OPENAI_AGENT_MODEL")
        return ChatOpenAI(
            model=OPENAI_AGENT_MODEL,
            api_key=OPENAI_API_KEY
        )
        
    validate_env_vars("GOOGLE_API_KEY", "GOOGLE_AGENT_MODEL")
    return ChatGoogleGenerativeAI(
        model=GOOGLE_AGENT_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

def get_embedding_model(provider: str = None) -> Embeddings:
    """
    Factory function to create embedding model instance based on the configured provider.
    
    Args:
        provider: Optional provider name ("openai" or "google"). 
                 If not provided, uses EMBEDDING_PROVIDER from config.
    
    Returns:
        Embeddings: configured embeddings instance (OpenAI or Google).
    
    Raises:
        SystemExit: If the provider is not supported, display a friendly message and exit.
    """
    normalized_provider = validate_provider(provider)
    
    if normalized_provider == "openai":
        validate_env_vars("OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL")
        return OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY,
            max_retries=3,
            request_timeout=60
        )

    validate_env_vars("GOOGLE_API_KEY", "GOOGLE_EMBEDDING_MODEL")
    return GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

