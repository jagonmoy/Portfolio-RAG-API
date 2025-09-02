import logging
import os
import shutil
import tempfile
from fastapi import HTTPException, UploadFile

from app.models.schemas import DocumentUploadResponse
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store_service

logger = logging.getLogger(__name__)


class DocumentController:
    def __init__(self):
        self.document_processor = document_processor
        self.vector_store_service = vector_store_service

    async def handle_upload(self, file: UploadFile) -> DocumentUploadResponse:
        try:
            if not self.vector_store_service.index:
                self.vector_store_service.initialize_vector_store()

            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                temp_path = temp_file.name

            documents = self.document_processor.process_file(temp_path)

            if documents:
                self.vector_store_service.add_documents(documents)

            os.unlink(temp_path)

            return DocumentUploadResponse(
                success=True,
                message=f"Successfully processed {len(documents)} documents",
                documents_added=len(documents)
            )

        except Exception as e:
            logger.error(f"Document upload failed: {str(e)}")
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise HTTPException(status_code=500, detail=f"Document upload failed: {str(e)}")

document_controller = DocumentController()