import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config.constants import PDF_PATH
from config.validation import validate_env_vars
from config.database import get_doc_storage

def ingest_pdf():
    """
    Ingest the PDF file into a vector database to use for an AI agent.
    The PDF files is internal and your location is defined in the .env file.
    If the path does not exist or is not a file, an error will be raised.
    The document will be split into chunks of 1000 characters with 150 characters of overlap and
    will be enriched with the metadata of the original document.
    """
    
    validate_env_vars("PDF_PATH")

    if not PDF_PATH.exists():
        raise FileNotFoundError(f"O arquivo PDF não foi encontrado em '{PDF_PATH}'")

    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"O caminho {PDF_PATH} não representa um arquivo")

    documents = PyPDFLoader(PDF_PATH).load()
    parts = split_document(documents)

    if not parts:
        raise SystemExit(0)

    enriched = enrich_document(parts)
    save_documents(enriched)

def split_document(documents: list[Document], chunk_size: int = 1000, chunk_overlap: int = 150) -> list[Document]:
    """
    Split the document into chunks of 1000 characters with 150 characters of overlap by default.

    Args:
        documents: The list of documents (pages) to split.
        chunk_size: The size of the chunks to split the documents into (default: 1000).
        chunk_overlap: The overlap of the chunks to split the documents into (default: 150).

    Returns:
        The list of documents split into chunks.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=False, # Data will be indexed manually while inserting
    ).split_documents(documents)

def enrich_document(documents: list[Document]) -> list[Document]:
    """
    Enrich the document with the metadata of the original document.

    Args:
        documents: The list of documents (pages) to enrich.

    Returns:
        The list of documents enriched with the metadata of the original document.
    """

    return [
        Document(
            page_content=doc.page_content,
            metadata={ key: value for key, value in doc.metadata.items() if value not in ("", None) },
        )
        for doc in documents
    ]

def save_documents(documents: list[Document], batch_size: int = 50, delay: float = 60):
    """
    Save the documents into a vector database in batches with delays to avoid rate limiting.
    
    Args:
        documents: The list of documents to save.
        batch_size: Number of documents to process per batch (default: 50).
        delay: Delay in seconds between batches (default: 60).
    """
    doc_storage = get_doc_storage()
    
    print(f"Iniciando ingestão em lotes de {batch_size} documentos com intervalo de {delay} segundos entre lotes...")

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        identifiers = [f"doc-{i + j}" for j in range(len(batch))]
        
        try:
            doc_storage.add_documents(documents=batch, ids=identifiers)
            print(f"Lote {i // batch_size + 1}/{(len(documents) + batch_size - 1) // batch_size} processado com sucesso!")
            
            if i + batch_size < len(documents):
                time.sleep(delay)
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                print(f"Limite de serviço atingido. Aguardando {delay * 2} segundos antes de tentar novamente...")
                time.sleep(delay * 2)
                doc_storage.add_documents(documents=batch, ids=identifiers)
            else:
                raise

    print("Ingestão de documentos concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()