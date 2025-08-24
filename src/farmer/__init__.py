"""
Farmer AI Agriculture Assistant

A comprehensive AI-powered chatbot designed to help farmers with agricultural advice,
weather information, crop disease detection, and market insights.
"""

__version__ = "1.0.0"
__author__ = "Gopal Bhingewad"
__email__ = "gopal@example.com"
__description__ = "AI Agriculture Assistant for Farmers"

from .app import create_app
from .config.settings import get_config, config
from .config.logging_config import setup_logging, get_logger

__all__ = [
    'create_app',
    'get_config',
    'config',
    'setup_logging',
    'get_logger'
]

# Initialize logging when package is imported
logger = get_logger(__name__)
logger.info(f"Farmer AI Agriculture Assistant v{__version__} initialized")
