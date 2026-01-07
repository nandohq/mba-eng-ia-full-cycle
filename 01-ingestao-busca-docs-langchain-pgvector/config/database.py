from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector

from .config import get_embedding_model
from .constants import PGVECTOR_URL, PGVECTOR_COLLECTION
from .validation import validate_env_vars

def get_doc_storage(embeddings: Embeddings = None, provider: str = None) -> PGVector:
    """
    Factory function to create PGVector document storage instance.
    
    Args:
        embeddings: Optional embeddings instance. If not provided, creates a new one.
        provider: Optional provider name ("openai" or "google").
                 Only used if embeddings is None.
    
    Returns:
        PGVector: configured document storage instance.
    
    Raises:
        ValueError: if PGVECTOR_URL or PGVECTOR_COLLECTION are not set.
    """
    validate_env_vars("PGVECTOR_URL", "PGVECTOR_COLLECTION")
    
    if embeddings is None:
        embeddings = get_embedding_model(provider)
    
    return PGVector(
        embeddings=embeddings,
        collection_name=PGVECTOR_COLLECTION,
        connection=PGVECTOR_URL,
        use_jsonb=True,
    )

