from typing import Any, Dict, List

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str

class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceDocument] = []

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    documents_added: int = 0

class HealthResponse(BaseModel):
    status: str
    service: str
