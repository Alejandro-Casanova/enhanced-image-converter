import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import colorama

colorama.init(autoreset=True)

class ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "DEBUG": colorama.Fore.CYAN,
        "INFO": colorama.Fore.WHITE,
        "CRITICAL": colorama.Fore.MAGENTA
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + str(record.msg)
        return logging.Formatter.format(self, record)
    
def init_logger(output_log_file: str = "logs/log",
                log_file_max_size: int = 102400,
                verbose: bool = False):
    """Initializes the logger with the specified parameters. The logger will log to both the console and a file.

    Args:
        output_log_file (str, optional): Path to log file. Defaults to "logs/log". If None, no file logging will be done.
        log_file_max_size (int, optional): Max byte size of log files before being automatically incremented. Defaults to 102400.
        verbose (bool, optional): Inits logger level to "debug" when true. Otherwise, inits to level "info". Defaults to False.
    """
    
    handlers = []

    # Make Directories if they don't exist
    if output_log_file is not None:
        os.makedirs(Path(output_log_file).parent.absolute(), exist_ok=True)
    
    # Create a formatter to define the log format
    logger_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s: %(message)s' if verbose else '%(levelname)s: %(message)s',
                                            datefmt='%H:%M:%S',)
    logger_level = logging.DEBUG if verbose else logging.INFO

    # Create a file handler to write logs to a file
    if output_log_file is not None:
        file_handler = RotatingFileHandler(output_log_file,
                                        maxBytes = log_file_max_size,
                                        backupCount = 100)
        file_handler.setLevel(logger_level)
        file_handler.setFormatter(logger_formatter)
        handlers.append(file_handler)

    # Create a stream handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)  # You can set the desired log level for console output
    console_handler.setFormatter(logger_formatter)
    handlers.append(console_handler)
    
    logging.basicConfig(level=logger_level,
                        handlers=handlers)

def init_logger_minimal(
    verbose: bool = False,
    color: bool = False,
) -> None:
    """
    Initializes the logger with the specified parameters. The logger will log to the console only.

    Args:
        verbose (bool, optional): Inits logger level to "debug" when true. Otherwise, inits to level "info". Defaults to False.
        color (bool, optional): Whether to enable colored output. Defaults to False.
    """
    
    # Create a formatter to define the log format
    print_format = '%(asctime)s %(levelname)s:%(name)s: %(message)s' if verbose else '%(levelname)s: %(message)s'
    if color:
        colorama.init(autoreset=True)
        logger_formatter = ColorFormatter(print_format, datefmt='%H:%M:%S')
    else:
        logger_formatter = logging.Formatter(fmt=print_format, datefmt='%H:%M:%S')
    
    logger_level = logging.DEBUG if verbose else logging.INFO

    # Create a stream handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)  # You can set the desired log level for console output
    console_handler.setFormatter(logger_formatter)
    
    logging.basicConfig(level=logger_level,
                        handlers=[console_handler])