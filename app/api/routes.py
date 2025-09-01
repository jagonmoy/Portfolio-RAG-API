import os
import shutil
import tempfile
import time

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.core.logging import StructuredLogger
from app.models.schemas import (
    DocumentUploadResponse,
    HealthResponse,
    QueryRequest,
    QueryResponse,
    SourceDocument,
)
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store_service

router = APIRouter()
logger = StructuredLogger(__name__)
settings = get_settings()

@router.post("/query", response_model=QueryResponse)
async def query_portfolio(request: QueryRequest):
    start_time = time.time()


    try:
        if not vector_store_service.index:
            vector_store_service.initialize_vector_store()

        query_engine = vector_store_service.get_query_engine(similarity_top_k=5)

        logger.info("Processing query",
                   question=request.question[:100],
                   max_tokens=request.max_tokens)

        response = query_engine.query(request.question)

        sources = []
        if hasattr(response, 'source_nodes') and response.source_nodes:
            for node in response.source_nodes:
                source_doc = SourceDocument(
                    content=node.node.text[:300] + "..." if len(node.node.text) > 300 else node.node.text,
                    metadata=node.node.metadata or {},
                    relevance_score=node.score if hasattr(node, 'score') else None
                )
                sources.append(source_doc)

        response_time = time.time() - start_time

        if response_time > settings.max_response_time:
            logger.warning("Slow response detected", response_time=response_time)

        query_response = QueryResponse(
            answer=str(response),
            sources=sources,
            response_time=response_time,
            tokens_used=len(str(response).split())  # Rough estimation
        )

        logger.info("Query completed successfully",
                   response_time=response_time,
                   sources_count=len(sources))

        return query_response

    except Exception as e:
        logger.error("Query failed", error=str(e), question=request.question[:50])
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    metadata: str = None
):
    try:
        if not vector_store_service.index:
            vector_store_service.initialize_vector_store()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        try:
            import json
            doc_metadata = json.loads(metadata) if metadata else {}
        except:
            doc_metadata = {}

        documents = document_processor.process_file(temp_path, doc_metadata)

        if documents:
            vector_store_service.add_documents(documents)

        os.unlink(temp_path)

        logger.info("Document uploaded successfully",
                   filename=file.filename,
                   docs_added=len(documents))

        return DocumentUploadResponse(
            success=True,
            message=f"Successfully processed {len(documents)} documents",
            documents_added=len(documents)
        )

    except Exception as e:
        logger.error("Document upload failed", error=str(e), filename=file.filename)
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=f"Document upload failed: {str(e)}")

@router.post("/documents/github", response_model=DocumentUploadResponse)
async def process_github_repo(repo_url: str):
    try:
        if not vector_store_service.index:
            vector_store_service.initialize_vector_store()

        documents = document_processor.process_github_repo(repo_url)

        if documents:
            vector_store_service.add_documents(documents)

        logger.info("GitHub repository processed",
                   repo_url=repo_url,
                   docs_added=len(documents))

        return DocumentUploadResponse(
            success=True,
            message=f"Successfully processed repository: {repo_url}",
            documents_added=len(documents)
        )

    except Exception as e:
        logger.error("GitHub repo processing failed", error=str(e), repo_url=repo_url)
        raise HTTPException(status_code=500, detail=f"GitHub repo processing failed: {str(e)}")

@router.post("/documents/portfolio", response_model=DocumentUploadResponse)
async def process_portfolio_site(url: str = "https://jagonmoy.github.io"):
    try:
        if not vector_store_service.index:
            vector_store_service.initialize_vector_store()

        documents = document_processor.process_portfolio_website(url)

        if documents:
            vector_store_service.add_documents(documents)

        logger.info("Portfolio website processed",
                   url=url,
                   docs_added=len(documents))

        return DocumentUploadResponse(
            success=True,
            message=f"Successfully processed portfolio website: {url}",
            documents_added=len(documents)
        )

    except Exception as e:
        logger.error("Portfolio site processing failed", error=str(e), url=url)
        raise HTTPException(status_code=500, detail=f"Portfolio site processing failed: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        doc_count = vector_store_service.get_document_count()

        return HealthResponse(
            status="healthy",
            service="portfolio-rag-api",
            vector_store_docs=doc_count,
            uptime="running"
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")

@router.get("/documents/count")
async def get_document_count():
    try:
        count = vector_store_service.get_document_count()
        return {"document_count": count}
    except Exception as e:
        logger.error("Failed to get document count", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get document count")
