import logging
import os
import inspect
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Utility functions remain as provided...

class AbstractLogger:
    def __init__(self, name=None, log_file=None, *args, **kwargs):
        self.stack_info = get_caller_info()
        name = name or self.stack_info['functionName'] or self.stack_info['fileName']
        log_file = log_file or f"{self.stack_info['fileName']}.app"
        self.logger = setup_logger(name, log_file)

    def mlog(self, message):
        self.log(message=message)

    def format_for_detail(self, message="", log_type='message'):
        stack_info = get_caller_info()
        return (f"\nTime: {time.asctime()}\nLocation: {stack_info['filePath']}, function: {stack_info['functionName']}"
                f"\nScript: {stack_info['fileName']}\n{log_type.capitalize()}: {message}\nLine No: {stack_info['lineNumber']}")

    def log(self, *args, **kwargs):
        """Logs a message at the specified level."""
        level = get_kwarg(['critical', 'info', 'warning', 'error', 'debug'], *args, **kwargs) or 'info'
        kwargs, detail = get_from_kwarg('detail', kwargs) or False
        message = get_not_arg(level, *args, **kwargs)

        if detail:
            message = self.format_for_detail(message, log_type=level)

        # Log action details before the actual log
        self.log_action_details(level, message)

        # Log the actual message
        if level.lower() == 'info':
            self.logger.info(message)
        elif level.lower() == 'error':
            self.logger.error(message)
        elif level.lower() == 'warning':
            self.logger.warning(message)
        elif level.lower() == 'debug':
            self.logger.debug(message)
        elif level.lower() == 'critical':
            self.logger.critical(message)
        else:
            self.logger.info(message)  # Default to info if an unrecognized level is given

    def log_action_details(self, level, message):
        """Logs details of the action being sent."""
        caller_info = get_caller_info()
        action_info = (f"Sending log action:\nLevel: {level.capitalize()}\n"
                       f"Message: {message}\n"
                       f"Called from {caller_info['functionName']} at {caller_info['filePath']}:{caller_info['lineNumber']}")
        self.logger.debug(action_info)  # You can change this level if needed

# Example usage
if __name__ == "__main__":
    logger = AbstractLogger("example_logger", "example.log")
    logger.log("This is an info message", detail=True)
    logger.log("A critical error occurred!", level='critical', detail=True)
    logger.log("A warning with no extra detail", level='warning')
