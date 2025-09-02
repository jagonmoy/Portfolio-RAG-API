from fastapi import APIRouter, File, UploadFile

from app.models.schemas import (
    DocumentUploadResponse,
    HealthResponse,
    QueryRequest,
    QueryResponse,
)
from app.controllers.query_controller import query_controller
from app.controllers.document_controller import document_controller
from app.controllers.health_controller import health_controller

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_portfolio(request: QueryRequest):
    return await query_controller.handle_query(request)

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    return await document_controller.handle_upload(file)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return await health_controller.handle_health_check()
