"""
Configuration settings for the Farmer AI Agriculture Assistant
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600

@dataclass
class RedisConfig:
    """Redis configuration settings"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    decode_responses: bool = True

@dataclass
class APIConfig:
    """API configuration settings"""
    openai_key: str
    huggingface_key: str
    weather_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3

@dataclass
class ServerConfig:
    """Server configuration settings"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    threaded: bool = True
    secret_key: str = "dev-secret-key-change-in-production"

@dataclass
class FileConfig:
    """File handling configuration"""
    upload_folder: str = "uploads"
    max_file_size: int = 16 * 1024 * 1024  # 16MB
    allowed_extensions: set = None
    audio_folder: str = "static/audio"
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = {'webm', 'jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav'}

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = "INFO"
    format: str = "detailed"
    directory: str = "logs"
    console_output: bool = True
    file_output: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    json_format: bool = False

@dataclass
class AgricultureConfig:
    """Agriculture-specific configuration"""
    supported_languages: Dict[str, str] = None
    seasons: Dict[str, Dict[str, Any]] = None
    soil_types: Dict[str, str] = None
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = {
                'en': 'English',
                'hi': 'हिंदी',
                'ta': 'தமிழ்',
                'te': 'తెలుగు',
                'bn': 'বাংলা',
                'mr': 'मराठी',
                'gu': 'ગુજરાતી',
                'kn': 'ಕನ್ನಡ',
                'ml': 'മലയാളം',
                'pa': 'ਪੰਜਾਬੀ'
            }
        
        if self.seasons is None:
            self.seasons = {
                'kharif': {
                    'period': 'June-September',
                    'crops': ['Rice', 'Maize', 'Cotton', 'Groundnut', 'Sugarcane'],
                    'practices': ['Sow before monsoon', 'Ensure proper drainage', 'Monitor for pests']
                },
                'rabi': {
                    'period': 'October-March',
                    'crops': ['Wheat', 'Barley', 'Mustard', 'Peas', 'Gram'],
                    'practices': ['Prepare soil well', 'Use irrigation', 'Protect from frost']
                },
                'zaid': {
                    'period': 'March-June',
                    'crops': ['Cucumber', 'Watermelon', 'Muskmelon', 'Bitter gourd'],
                    'practices': ['Use irrigation', 'Provide shade', 'Harvest early']
                }
            }
        
        if self.soil_types is None:
            self.soil_types = {
                'clay': 'Good water retention, suitable for rice and wheat',
                'sandy': 'Good drainage, suitable for groundnuts and potatoes',
                'loamy': 'Best for most crops, balanced properties',
                'black': 'Rich in minerals, good for cotton and sugarcane'
            }

class Config:
    """Main configuration class"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables and defaults"""
        
        # Database configuration
        self.database = DatabaseConfig(
            url=os.getenv('DATABASE_URL', 'postgresql://farmer_user:farmer_password@postgres:5432/farmer'),
            echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true',
            pool_size=int(os.getenv('DATABASE_POOL_SIZE', '10')),
            max_overflow=int(os.getenv('DATABASE_MAX_OVERFLOW', '20')),
            pool_timeout=int(os.getenv('DATABASE_POOL_TIMEOUT', '30')),
            pool_recycle=int(os.getenv('DATABASE_POOL_RECYCLE', '3600'))
        )
        
        # Redis configuration
        self.redis = RedisConfig(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', '6379')),
            db=int(os.getenv('REDIS_DB', '0')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=os.getenv('REDIS_DECODE_RESPONSES', 'true').lower() == 'true'
        )
        
        # API configuration
        self.api = APIConfig(
            openai_key=os.getenv('OPENAI_API_KEY') or os.getenv('open_ai_key'),
            huggingface_key=os.getenv('HUGGINGFACE_KEY') or os.getenv('hugging_face'),
            weather_key=os.getenv('WEATHER_API_KEY') or os.getenv('weather_api_key'),
            timeout=int(os.getenv('API_TIMEOUT', '30')),
            max_retries=int(os.getenv('API_MAX_RETRIES', '3'))
        )
        
        # Server configuration
        self.server = ServerConfig(
            host=os.getenv('FARMER_HOST', '0.0.0.0'),
            port=int(os.getenv('FARMER_PORT', '8000')),
            debug=os.getenv('FARMER_DEBUG', 'false').lower() == 'true',
            threaded=os.getenv('FARMER_THREADED', 'true').lower() == 'true',
            secret_key=os.getenv('FARMER_SECRET_KEY') or os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        )
        
        # File configuration
        self.file = FileConfig(
            upload_folder=os.getenv('FARMER_UPLOAD_FOLDER', 'uploads'),
            max_file_size=int(os.getenv('FARMER_MAX_FILE_SIZE', str(16 * 1024 * 1024))),
            audio_folder=os.getenv('FARMER_AUDIO_FOLDER', 'static/audio')
        )
        
        # Logging configuration
        self.logging = LoggingConfig(
            level=os.getenv('FARMER_LOG_LEVEL', 'INFO'),
            format=os.getenv('FARMER_LOG_FORMAT', 'detailed'),
            directory=os.getenv('FARMER_LOG_DIR', 'logs'),
            console_output=os.getenv('FARMER_CONSOLE_LOG', 'true').lower() == 'true',
            file_output=os.getenv('FARMER_FILE_LOG', 'true').lower() == 'true',
            max_file_size=int(os.getenv('FARMER_LOG_MAX_SIZE', str(10 * 1024 * 1024))),
            backup_count=int(os.getenv('FARMER_LOG_BACKUP_COUNT', '5')),
            json_format=os.getenv('FARMER_JSON_LOG', 'false').lower() == 'true'
        )
        
        # Agriculture configuration
        self.agriculture = AgricultureConfig()
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check required API keys
        if not self.api.openai_key:
            errors.append("OpenAI API key is required")
        
        if not self.api.huggingface_key:
            errors.append("Hugging Face API key is required")
        
        # Check file paths
        if not os.path.exists(self.file.upload_folder):
            try:
                os.makedirs(self.file.upload_folder, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create upload folder: {e}")
        
        if not os.path.exists(self.file.audio_folder):
            try:
                os.makedirs(self.file.audio_folder, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create audio folder: {e}")
        
        # Check database URL
        if not self.database.url:
            errors.append("Database URL is required")
        
        # Redis is optional for local development
        # No validation needed
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def get_flask_config(self) -> Dict[str, Any]:
        """Get Flask configuration dictionary"""
        return {
            'SECRET_KEY': self.server.secret_key,
            'SQLALCHEMY_DATABASE_URI': self.database.url,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_size': self.database.pool_size,
                'max_overflow': self.database.max_overflow,
                'pool_timeout': self.database.pool_timeout,
                'pool_recycle': self.database.pool_recycle,
                'echo': self.database.echo
            },
            'UPLOAD_FOLDER': self.file.upload_folder,
            'MAX_CONTENT_LENGTH': self.file.max_file_size,
            'ALLOWED_EXTENSIONS': self.file.allowed_extensions
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'database': {
                'url': self.database.url,
                'echo': self.database.echo,
                'pool_size': self.database.pool_size,
                'max_overflow': self.database.max_overflow,
                'pool_timeout': self.database.pool_timeout,
                'pool_recycle': self.database.pool_recycle
            },
            'redis': {
                'host': self.redis.host,
                'port': self.redis.port,
                'db': self.redis.db,
                'password': '***' if self.redis.password else None,
                'decode_responses': self.redis.decode_responses
            },
            'api': {
                'openai_key': '***' if self.api.openai_key else None,
                'huggingface_key': '***' if self.api.huggingface_key else None,
                'weather_key': '***' if self.api.weather_key else None,
                'timeout': self.api.timeout,
                'max_retries': self.api.max_retries
            },
            'server': {
                'host': self.server.host,
                'port': self.server.port,
                'debug': self.server.debug,
                'threaded': self.server.threaded
            },
            'file': {
                'upload_folder': self.file.upload_folder,
                'max_file_size': self.file.max_file_size,
                'audio_folder': self.file.audio_folder,
                'allowed_extensions': list(self.file.allowed_extensions)
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'directory': self.logging.directory,
                'console_output': self.logging.console_output,
                'file_output': self.logging.file_output,
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count,
                'json_format': self.logging.json_format
            },
            'agriculture': {
                'supported_languages': self.agriculture.supported_languages,
                'seasons': self.agriculture.seasons,
                'soil_types': self.agriculture.soil_types
            }
        }

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config

def reload_config():
    """Reload configuration from environment variables"""
    global config
    config = Config()
    return config

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    def __init__(self):
        super().__init__()
        self.server.debug = True
        self.logging.level = 'DEBUG'
        self.database.echo = True

class ProductionConfig(Config):
    """Production configuration"""
    def __init__(self):
        super().__init__()
        self.server.debug = False
        self.logging.level = 'WARNING'
        self.database.echo = False

class TestingConfig(Config):
    """Testing configuration"""
    def __init__(self):
        super().__init__()
        self.server.debug = True
        self.logging.level = 'DEBUG'
        self.database.url = 'sqlite:///:memory:'
        self.database.echo = False

# Configuration factory
def get_config_by_env(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    config_class = configs.get(env, DevelopmentConfig)
    return config_class()

# Auto-load configuration
if __name__ == '__main__':
    # Print configuration for debugging
    print("Current configuration:")
    import json
    print(json.dumps(config.to_dict(), indent=2, default=str))
