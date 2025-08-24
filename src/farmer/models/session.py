"""
User session model for tracking user sessions
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from typing import Optional

from .chat import Base
from ..config.logging_config import get_logger

logger = get_logger(__name__)

class UserSession(Base):
    """User session model for tracking user sessions"""
    
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    device_info = Column(Text, nullable=True)  # JSON string for device information
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __init__(self, **kwargs):
        """Initialize session with logging"""
        super().__init__(**kwargs)
        logger.debug(f"Creating new session: {self.session_id} for user {self.user_id}")
        
        if hasattr(self, 'user_id') and self.user_id:
            logger.info(f"New session started for user {self.user_id}")
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
        logger.debug(f"Updated activity for session {self.session_id}")
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return True
        return False
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'device_info': self.device_info,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
    
    def __repr__(self):
        return f"<UserSession(session_id='{self.session_id}', user_id='{self.user_id}')>"
