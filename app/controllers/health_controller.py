from app.models.schemas import HealthResponse


class HealthController:
    async def handle_health_check(self) -> HealthResponse:
        return HealthResponse(
            status="healthy",
            service="minimal-rag-api"
        )

health_controller = HealthController()