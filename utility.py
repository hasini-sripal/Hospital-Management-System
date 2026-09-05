"""
Utility functions for Hospital Management System
"""
import CustomExceptions, logger, config_loader

def get_input_with_retry(prompt:str, validator:callable, exceptions:tuple, max_tries:int=5, **kwargs:dict)-> str | None:
    """
    Generic input function with retry logic
    """
    max_tries = kwargs.get('max_tries', max_tries)
    error_prefix = kwargs.get('error_prefix', 'Error: ')
    for trial in range(1, max_tries + 1):
        try:
            value = input(prompt)
            validator(value)
            return value
        except exceptions as e:
            print(f"{error_prefix}:{e}")
        
        if trial == max_tries:
            print("Discarding input. Returning to menu.")
            return None
    return None

def timer(function:callable) -> callable:
    """
    Decorator to measure the execution time of a function.
    """
    import time
    def wrapper(*args:any, **kwargs:any) -> any:
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        print(f"{function.__name__} completed in {time_taken:.3f} seconds")
        return result
    return wrapper

def log_action(function:callable) -> callable:
    """
    Decorator to log the execution of a function.
    """
    def wrapper(*args:any, **kwargs:any) -> any:
        logger_instance = logger.get_logger()
        logger_instance.info(f"Executing {function.__name__} with args: {args}, kwargs: {kwargs}")
        result = function(*args, **kwargs)
        logger_instance.info(f"Completed {function.__name__} with result: {result}")
        return result
    return wrapper
