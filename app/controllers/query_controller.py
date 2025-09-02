import logging
from fastapi import HTTPException

from app.models.schemas import QueryRequest, QueryResponse, SourceDocument
from app.services.vector_store import vector_store_service

logger = logging.getLogger(__name__)


class QueryController:
    def __init__(self):
        self.vector_store_service = vector_store_service

    async def handle_query(self, request: QueryRequest) -> QueryResponse:
        try:
            if not self.vector_store_service.index:
                self.vector_store_service.initialize_vector_store()

            query_engine = self.vector_store_service.get_query_engine()
            response = query_engine.query(request.question)

            sources = []
            if hasattr(response, 'source_nodes') and response.source_nodes:
                for node in response.source_nodes:
                    source_doc = SourceDocument(
                        content=node.node.text[:200] + "..." if len(node.node.text) > 200 else node.node.text,
                        metadata=node.node.metadata or {}
                    )
                    sources.append(source_doc)

            return QueryResponse(
                answer=str(response),
                sources=sources
            )

        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

query_controller = QueryController()