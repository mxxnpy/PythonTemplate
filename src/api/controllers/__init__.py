# controllers
from src.api.controllers.health_controller import router as health_router
from src.api.controllers.example_controller import router as example_router

__all__ = ["health_router", "example_router"]

