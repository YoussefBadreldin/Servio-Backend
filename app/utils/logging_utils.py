import time
from typing import Callable

def log_execution(func: Callable) -> Callable:
    """
    Decorator to log function execution.
    """
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Execution complete. Result: {result if len(str(result)) < 100 else '...'}")
        return result
    return wrapper

def track_performance(func: Callable) -> Callable:
    """
    Decorator to track function performance.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper