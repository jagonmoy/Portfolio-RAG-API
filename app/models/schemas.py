from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="The question to ask about Jagonmoy's background")
    max_tokens: Optional[int] = Field(default=200, ge=50, le=500, description="Maximum tokens in response")
    temperature: Optional[float] = Field(default=0.1, ge=0.0, le=1.0, description="Response creativity (0=focused, 1=creative)")

class SourceDocument(BaseModel):
    content: str = Field(..., description="Relevant content from the source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    relevance_score: Optional[float] = Field(default=None, description="Relevance score for this source")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used")
    response_time: float = Field(..., description="Time taken to generate response in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was generated")
    tokens_used: Optional[int] = Field(default=None, description="Tokens used in the response")

class DocumentUploadRequest(BaseModel):
    file_path: str = Field(..., description="Path to the document file")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata for the document")

class DocumentUploadResponse(BaseModel):
    success: bool = Field(..., description="Whether the upload was successful")
    message: str = Field(..., description="Status message")
    documents_added: int = Field(default=0, description="Number of documents added to the vector store")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    vector_store_docs: int = Field(default=0, description="Number of documents in vector store")
    uptime: str = Field(default="unknown", description="Service uptime")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")
