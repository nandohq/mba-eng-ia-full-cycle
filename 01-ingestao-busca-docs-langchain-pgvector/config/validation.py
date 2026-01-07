import os
import sys
from typing import Literal
from config.constants import EMBEDDING_PROVIDER

SupportedProviders = Literal["openai", "google"]
SUPPORTED_PROVIDERS = ["openai", "google"]


def _get_default_provider() -> str:
    """
    Get the default embedding provider from environment variable.
    
    Returns:
        str: Default provider name (defaults to "openai" if not set).
    """
    return EMBEDDING_PROVIDER

def validate_provider(provider: str = None) -> str:
    """
    Validate if the provider is supported.
    
    Args:
        provider: Name of the provider to be validated.
        If not provided, uses EMBEDDING_PROVIDER from environment variable.
    
    Returns:
        str: Normalized provider name.
    
    Raises:
        SystemExit: If the provider is not supported, display a friendly message and exit.
    """
    normalized_provider = (provider or _get_default_provider())

    if normalized_provider not in SUPPORTED_PROVIDERS:
        print("\n" + "="*60, file=sys.stderr)
        print("Erro: provedor de embedding não suportado!", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(
            f"\nO provedor de embedding '{normalized_provider}' não é suportado. "
            f"Utilize {', '.join(SUPPORTED_PROVIDERS)}\n",
            file=sys.stderr
        )
        print("-"*60, file=sys.stderr)
        sys.exit(1)

    return normalized_provider

def validate_env_vars(*required_vars: str) -> None:
    """
    Validate if the necessary environment variables are set.
    
    Args:
        *required_vars: environment variables to be validated.
    
    Raises:
        SystemExit: if any of the environment variables are not set.
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("\n" + "="*60, file=sys.stderr)
        print("Erro: variáveis de ambiente não configuradas!", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print("\nAs seguintes variáveis de ambiente estão faltando:\n", file=sys.stderr)
        
        for var in missing_vars:
            print(f"  • {var}", file=sys.stderr)
        
        print("\n" + "-"*60, file=sys.stderr)
        sys.exit(1)