"""
Logging configuration for the Farmer AI Agriculture Assistant
"""
import os
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime

# Log levels
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Log formats
LOG_FORMATS = {
    'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
    'simple': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'json': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(extra)s'
}

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'extra'):
            log_entry['extra'] = record.extra
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, default=str)

class ColoredFormatter(logging.Formatter):
    """Custom colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logging(
    log_level: str = 'INFO',
    log_format: str = 'detailed',
    log_dir: str = 'logs',
    console_output: bool = True,
    file_output: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    json_format: bool = False
) -> None:
    """
    Set up logging configuration for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format style (detailed, simple, json)
        log_dir: Directory to store log files
        console_output: Enable console logging
        file_output: Enable file logging
        max_file_size: Maximum size of log files before rotation
        backup_count: Number of backup files to keep
        json_format: Use JSON format for structured logging
    """
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    if json_format:
        formatter = JSONFormatter()
        file_formatter = JSONFormatter()
    else:
        formatter = ColoredFormatter(LOG_FORMATS[log_format])
        file_formatter = logging.Formatter(LOG_FORMATS[log_format])
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handlers
    if file_output:
        # Main application log
        app_log_file = log_path / f"farmer_{datetime.now().strftime('%Y%m%d')}.log"
        app_handler = logging.handlers.RotatingFileHandler(
            app_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        app_handler.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
        app_handler.setFormatter(file_formatter)
        root_logger.addHandler(app_handler)
        
        # Error log (only errors and critical)
        error_log_file = log_path / f"farmer_errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
        
        # Access log for web requests
        access_log_file = log_path / f"farmer_access_{datetime.now().strftime('%Y%m%d')}.log"
        access_handler = logging.handlers.RotatingFileHandler(
            access_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(file_formatter)
        
        # Create access logger
        access_logger = logging.getLogger('farmer.access')
        access_logger.addHandler(access_handler)
        access_logger.propagate = False
    
    # Set specific logger levels
    logging.getLogger('farmer').setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    logging.getLogger('farmer.api').setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    logging.getLogger('farmer.core').setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    logging.getLogger('farmer.services').setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    
    # Reduce noise from external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('cv2').setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def log_function_call(logger: logging.Logger, func_name: str, **kwargs):
    """
    Decorator helper to log function calls
    
    Args:
        logger: Logger instance
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    logger.debug(f"Calling {func_name} with parameters: {kwargs}")

def log_function_result(logger: logging.Logger, func_name: str, result: Any):
    """
    Log function results
    
    Args:
        logger: Logger instance
        func_name: Name of the function
        result: Function result to log
    """
    logger.debug(f"{func_name} returned: {result}")

def log_error_with_context(logger: logging.Logger, error: Exception, context: str = "", **kwargs):
    """
    Log errors with additional context
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context information
        **kwargs: Additional key-value pairs to log
    """
    extra_info = f"Context: {context}" if context else ""
    if kwargs:
        extra_info += f" | Additional info: {kwargs}"
    
    logger.error(f"{error.__class__.__name__}: {str(error)} | {extra_info}", exc_info=True)

# Convenience functions for common logging patterns
def log_api_request(logger: logging.Logger, method: str, endpoint: str, user_id: str = None, **kwargs):
    """Log API request details"""
    extra = f"User: {user_id}" if user_id else ""
    if kwargs:
        extra += f" | {kwargs}"
    logger.info(f"API Request: {method} {endpoint} | {extra}")

def log_api_response(logger: logging.Logger, method: str, endpoint: str, status_code: int, response_time: float, **kwargs):
    """Log API response details"""
    extra = f"Response time: {response_time:.3f}s"
    if kwargs:
        extra += f" | {kwargs}"
    logger.info(f"API Response: {method} {endpoint} | Status: {status_code} | {extra}")

def log_database_operation(logger: logging.Logger, operation: str, table: str, record_id: str = None, **kwargs):
    """Log database operations"""
    extra = f"Record ID: {record_id}" if record_id else ""
    if kwargs:
        extra += f" | {kwargs}"
    logger.debug(f"Database {operation}: {table} | {extra}")

def log_file_operation(logger: logging.Logger, operation: str, file_path: str, file_size: int = None, **kwargs):
    """Log file operations"""
    extra = f"Size: {file_size} bytes" if file_size else ""
    if kwargs:
        extra += f" | {kwargs}"
    logger.debug(f"File {operation}: {file_path} | {extra}")

# Initialize logging with default configuration
def init_logging():
    """Initialize logging with default configuration"""
    # Check if logging is already configured
    if logging.getLogger().handlers:
        return
    
    # Get configuration from environment variables
    log_level = os.getenv('FARMER_LOG_LEVEL', 'INFO')
    log_format = os.getenv('FARMER_LOG_FORMAT', 'detailed')
    log_dir = os.getenv('FARMER_LOG_DIR', 'logs')
    console_output = os.getenv('FARMER_CONSOLE_LOG', 'true').lower() == 'true'
    file_output = os.getenv('FARMER_FILE_LOG', 'true').lower() == 'true'
    json_format = os.getenv('FARMER_JSON_LOG', 'false').lower() == 'true'
    
    setup_logging(
        log_level=log_level,
        log_format=log_format,
        log_dir=log_dir,
        console_output=console_output,
        file_output=file_output,
        json_format=json_format
    )

# Auto-initialize logging when module is imported
init_logging()
