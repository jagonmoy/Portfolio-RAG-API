import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import pypdf
from llama_index.core import Document

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {'.txt', '.md', '.pdf'}

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

    def process_pdf_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                all_text = ""
                page_count = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            all_text += f"\n--- Page {page_num} ---\n" + page_text
                    except Exception as page_e:
                        logger.warning(f"Failed to extract text from page {page_num}: {str(page_e)}")
                        continue

            if not all_text.strip():
                logger.warning(f"No text content extracted from PDF: {file_path}")
                return []

            doc_metadata = {
                "file_name": os.path.basename(file_path),
                "file_type": "pdf",
                "page_count": page_count,
                **(metadata or {})
            }

            document = Document(
                text=all_text.strip(),
                metadata=doc_metadata
            )

            logger.info(f"PDF file processed: {file_path} ({page_count} pages)")
            return [document]

        except Exception as e:
            logger.error(f"Failed to process PDF file {file_path}: {str(e)}")
            return []

    def process_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        file_extension = Path(file_path).suffix.lower()

        if file_extension in {'.txt', '.md'}:
            return self.process_text_file(file_path, metadata)
        elif file_extension == '.pdf':
            return self.process_pdf_file(file_path, metadata)
        else:
            logger.warning(f"Unsupported file format: {file_extension}")
            return []

document_processor = DocumentProcessor()
