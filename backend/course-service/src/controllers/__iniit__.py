# Controllers package initialization
from .courseController import router as course_router
from .prerequisiteController import router as prerequisite_router

__all__ = ["course_router", "prerequisite_router"]
