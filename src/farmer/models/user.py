"""
User model for storing user information
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from typing import Optional, List

from .chat import Base
from ..config.logging_config import get_logger

logger = get_logger(__name__)

class User(Base):
    """User model for storing user information"""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    language = Column(String(10), default='en')
    preferences = Column(Text, nullable=True)  # JSON string for user preferences
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    chat_history = relationship("ChatHistory", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    
    def __init__(self, **kwargs):
        """Initialize user with logging"""
        super().__init__(**kwargs)
        logger.debug(f"Creating new user: {self.user_id}")
        
        if hasattr(self, 'username') and self.username:
            logger.info(f"New user registered: {self.username} ({self.user_id})")
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        logger.debug(f"Updated last login for user {self.user_id}")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'language': self.language,
            'preferences': self.preferences,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}')>"
