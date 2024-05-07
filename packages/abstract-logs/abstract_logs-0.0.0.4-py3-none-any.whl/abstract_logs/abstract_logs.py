import logging
import os
import inspect
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
import logging,os, inspect,time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from abstract_utilities.read_write_utils import string_in_keys
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
def get_caller_info():
    """Retrieve the name and location of the calling function in the stack."""
    stack = inspect.stack()
    # stack[1] gives you the frame of the caller
    # stack[0] is this function itself
    parent_frame = stack[2]
    caller = parent_frame.frame
    filePath = caller.f_code.co_filename
    dirName = os.path.dirname(caller.f_code.co_filename)
    baseName = os.path.basename(caller.f_code.co_filename)
    fileName = os.path.splitext(baseName)
    fileName,ext = fileName[0],fileName[-1] if len(fileName)>1 else None
    info = {
        'functionName': parent_frame.function,
        'filePath': filePath,
        'lineNumber': parent_frame.lineno,
        'directory': dirName,
        'baseName': baseName,
        'fileName':fileName,
        'ext':ext,
    }
    return info

def example_function():
    # This function will call another function which fetches the caller's details
    return get_caller_info()

def get_not_arg(objs,*args,**kwargs):
    for val in list(args)+list(kwargs.values()):
        if val not in objs:
            return val
def get_kwarg(list_obj,*args,**kwargs):
    obj=None
    if kwargs:
        obj = string_in_keys(list_obj,kwargs)
    obj = obj or next((arg for arg in args if arg in list_obj), None)
    
    return obj

def get_error_msg(error_msg, default_error_msg):
    return error_msg if error_msg else default_error_msg
    
# Get the path to the user's documents directory
def get_documents_dir():
    try:
        # Try to use the platform's environment variables to find the documents directory
        from win32com.shell import shell, shellcon
        documents_path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
    except ImportError:
        # Fallback if the win32com module is not available (non-Windows systems)
        documents_path = str(Path.home() / "Documents")
    return documents_path

# Define the base directory for logs
LOG_DIR = Path(get_documents_dir()) / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
def get_file_name():
    curr_path = os.getcwd()
    baseName = os.path.basename(curr_path)
    splitExt = os.path.splitext(baseName)
    fileName = splitExt[0]
    if len(splitExt)>1:
        fileName,ext = splitExt
    return fileName
def get_from_args_kwargs(name,log_file,args,kwargs):
    if not (name and log_file):
        kwargs = [name,log_file]
        types=['_logger','.log']
        fileName = get_file_name()
        for i,kwarg in enumerate(kwargs):
            if kwarg == None:
                kwargs[i] = f"{fileName}{types[i]}"
        name,log_file = kwargs[0],kwargs[1]

def setup_logger(name, log_file, level=logging.DEBUG,rotate=True,consolHandle=True,standardFormat=True,fileHandler=True,streamHandle=True):
    """Function to set up a logger for a specified module"""
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Construct full path for the log file
    full_log_path = os.path.join(LOG_DIR, log_file)

    # Ensure the logger only has one handler attached
    if not logger.handlers:
        if standardFormat:
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Create rotating file handler
        if rotate:
            file_handler = RotatingFileHandler(full_log_path, maxBytes=1024*1024*5, backupCount=5)
        
        # Create formatter and add it to the handlers
        if standardFormat:
            file_handler.setFormatter(formatter)

        # Create console handler
        if streamHandle:
            console_handler = logging.StreamHandler()
        if consolHandle:
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)   
        # Add the handlers to the logger
        if fileHandler:
            file_handler.setLevel(level)
            logger.addHandler(file_handler)
    
    return logger
def get_from_kwarg(key,kwarg):
    value = kwarg.get(key)
    if value:
        del kwarg[key]
    return kwarg,value
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
