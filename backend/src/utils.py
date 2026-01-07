import logging
from typing import Any, Optional
from functools import wraps
import time

logger = logging.getLogger(__name__)

def handle_exceptions(func):
    """
    Decorator to handle exceptions and log them appropriately
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def log_execution_time(func):
    """
    Decorator to log the execution time of a function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper

def safe_execute(func, *args, default_return=None, **kwargs):
    """
    Safely execute a function, returning a default value if it fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Error in {func.__name__}: {str(e)}. Returning default value.")
        return default_return

class CustomException(Exception):
    """
    Custom exception class for the RAG pipeline
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted
    """
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None