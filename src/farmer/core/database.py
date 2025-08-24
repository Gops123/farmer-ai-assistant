"""
Database initialization and management
"""
from flask_sqlalchemy import SQLAlchemy
import logging

# Create SQLAlchemy instance
db = SQLAlchemy()

# Get logger
logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize database with Flask app"""
    try:
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            logger.info("Database initialized successfully")
            
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db():
    """Get database instance"""
    return db
