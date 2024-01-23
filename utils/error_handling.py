import logging


def log_error(error_message: str) -> None:
    """
    Log the given error message.
    
    Args:
        error_message (str): The error message to be logged.
    """
    logging.error(error_message)

def handle_error(error_message: str) -> None:
    """
    Handle the given error message by logging it and performing any necessary error handling actions.
    
    Args:
        error_message (str): The error message to be handled.
    """
    log_error(error_message)
    # Perform additional error handling actions if needed
