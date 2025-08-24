"""
Redis client initialization and management
"""
import redis
import logging
from typing import Optional
from ..config.settings import get_config

# Get logger
logger = logging.getLogger(__name__)

# Global Redis client
redis_client: Optional[redis.Redis] = None

def init_redis():
    """Initialize Redis client"""
    global redis_client
    
    try:
        config = get_config()
        
        redis_client = redis.Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            decode_responses=config.redis.decode_responses,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        
        # Test connection
        redis_client.ping()
        logger.info("Redis client initialized successfully")
        
    except Exception as e:
        logger.warning(f"Redis not available: {e}. Running without Redis cache.")
        redis_client = None

def get_redis() -> Optional[redis.Redis]:
    """Get Redis client instance"""
    global redis_client
    
    if redis_client is None:
        init_redis()
    
    return redis_client

def close_redis():
    """Close Redis connection"""
    global redis_client
    
    if redis_client:
        redis_client.close()
        redis_client = None
        logger.info("Redis connection closed")
