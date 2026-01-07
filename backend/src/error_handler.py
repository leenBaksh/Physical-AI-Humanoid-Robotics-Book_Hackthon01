import logging
from typing import Callable, Any
from functools import wraps
from fastapi import HTTPException, status
from .utils import CustomException

logger = logging.getLogger(__name__)

def handle_pipeline_errors(func: Callable) -> Callable:
    """
    Decorator to handle errors in the pipeline functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            logger.error(f"Custom exception in {func.__name__}: {e.message} (Code: {e.error_code})")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": e.message, "error_code": e.error_code}
            )
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Internal server error", "message": str(e)}
            )
    return wrapper

def setup_error_handlers(app):
    """
    Setup global error handlers for the FastAPI application
    """
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception: {str(exc)}", exc_info=True)
        return {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "An unexpected error occurred"
        }

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request, exc):
        logger.error(f"Custom exception: {exc.message} (Code: {exc.error_code})")
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": {"error": exc.message, "error_code": exc.error_code}
        }