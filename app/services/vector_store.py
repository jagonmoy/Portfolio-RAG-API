import os
from typing import List

import chromadb
from chromadb.config import Settings as ChromaSettings
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.core.config import get_settings
from app.core.logging import StructuredLogger

logger = StructuredLogger(__name__)
settings = get_settings()

class VectorStoreService:
    def __init__(self):
        self.chroma_client = None
        self.vector_store = None
        self.storage_context = None
        self.index = None
        self._setup_llama_index()

    def _setup_llama_index(self):
        Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            api_key=settings.openai_api_key,
            temperature=0.1
        )
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-ada-002",
            api_key=settings.openai_api_key
        )

    def initialize_vector_store(self) -> None:
        try:
            os.makedirs(settings.chroma_persist_path, exist_ok=True)

            self.chroma_client = chromadb.PersistentClient(
                path=settings.chroma_persist_path,
                settings=ChromaSettings(anonymized_telemetry=False)
            )

            chroma_collection = self.chroma_client.get_or_create_collection("portfolio_docs")

            self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

            existing_docs = chroma_collection.count()
            if existing_docs > 0:
                logger.info("Loading existing vector index", doc_count=existing_docs)
                self.index = VectorStoreIndex.from_vector_store(
                    vector_store=self.vector_store,
                    storage_context=self.storage_context
                )
            else:
                logger.info("Creating new vector index")
                self.index = VectorStoreIndex([], storage_context=self.storage_context)

        except Exception as e:
            logger.error("Failed to initialize vector store", error=str(e))
            raise

    def add_documents(self, documents: List[Document]) -> None:
        if not self.index:
            raise ValueError("Vector store not initialized")

        try:
            for doc in documents:
                self.index.insert(doc)
            logger.info("Documents added to vector store", count=len(documents))
        except Exception as e:
            logger.error("Failed to add documents", error=str(e))
            raise

    def get_query_engine(self, similarity_top_k: int = 5):
        if not self.index:
            raise ValueError("Vector store not initialized")

        return self.index.as_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode="compact"
        )

    def get_document_count(self) -> int:
        if not self.chroma_client:
            return 0

        try:
            collection = self.chroma_client.get_collection("portfolio_docs")
            return collection.count()
        except:
            return 0

vector_store_service = VectorStoreService()
