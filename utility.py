"""
Utility functions for Hospital Management System
"""
import CustomExceptions

def get_input_with_retry(prompt, validator, exceptions, max_tries=5):
    """
    Generic input function with retry logic
    """
    for trial in range(1, max_tries + 1):
        try:
            value = input(prompt)
            validator(value)
            return value
        except exceptions as e:
            print(f"Error: {e}")
        
        if trial == max_tries:
            print("Discarding input. Returning to menu.")
            return None
    return None

