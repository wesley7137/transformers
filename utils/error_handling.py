import logging
import traceback
from datetime import datetime


def handle_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack_trace = traceback.format_exc()
    
    logging.error(f"[{timestamp}] Error: {error_message}\n{stack_trace}")

def handle_exception(exception):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack_trace = traceback.format_exc()
    
    logging.exception(f"[{timestamp}] Exception: {str(exception)}\n{stack_trace}")
