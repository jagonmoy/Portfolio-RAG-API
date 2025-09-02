import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from llama_index.core import Document

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {'.txt', '.md'}

    def process_text_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            doc_metadata = {
                "file_name": os.path.basename(file_path),
                "file_type": Path(file_path).suffix[1:],
                **(metadata or {})
            }

            document = Document(
                text=content,
                metadata=doc_metadata
            )

            logger.info(f"Text file processed: {file_path}")
            return [document]

        except Exception as e:
            logger.error(f"Failed to process text file {file_path}: {str(e)}")
            return []

    def process_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        file_extension = Path(file_path).suffix.lower()

        if file_extension in {'.txt', '.md'}:
            return self.process_text_file(file_path, metadata)
        else:
            logger.warning(f"Unsupported file format: {file_extension}")
            return []

document_processor = DocumentProcessor()
