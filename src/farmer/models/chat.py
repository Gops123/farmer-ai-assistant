"""
Chat history model for storing user interactions
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict, Any
import json

from ..config.logging_config import get_logger

logger = get_logger(__name__)

Base = declarative_base()

class ChatHistory(Base):
    """Chat history model for storing user interactions"""
    
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    message_type = Column(String(20), default='text')  # text, voice, image
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    meta_data = Column(Text, nullable=True)  # JSON string for additional data
    response_time = Column(Integer, nullable=True)  # Response time in milliseconds
    error_occurred = Column(String(1), default='N')  # Y/N flag for errors
    
    # Relationships
    user = relationship("User", back_populates="chat_history", foreign_keys=[user_id])
    
    # Indexes for better query performance
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
        Index('idx_message_type', 'message_type'),
        Index('idx_error_flag', 'error_occurred'),
    )
    
    def __init__(self, **kwargs):
        """Initialize chat history entry with logging"""
        super().__init__(**kwargs)
        logger.debug(f"Creating new chat history entry for user {self.user_id}")
        
        # Log the creation
        if hasattr(self, 'message') and self.message:
            logger.info(f"New chat entry: User {self.user_id} sent {self.message_type} message")
    
    def set_metadata(self, data: Dict[str, Any]) -> None:
        """Set metadata as JSON string"""
        try:
            self.meta_data = json.dumps(data, default=str)
            logger.debug(f"Set metadata for chat entry {self.id}: {data}")
        except Exception as e:
            logger.error(f"Failed to set metadata for chat entry {self.id}: {e}")
            self.meta_data = json.dumps({'error': 'Failed to serialize metadata'})
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata as dictionary"""
        if not self.meta_data:
            return {}
        
        try:
            return json.loads(self.meta_data)
        except Exception as e:
            logger.error(f"Failed to parse metadata for chat entry {self.id}: {e}")
            return {'error': 'Failed to parse metadata'}
    
    def set_response_time(self, response_time_ms: int) -> None:
        """Set response time in milliseconds"""
        self.response_time = response_time_ms
        logger.debug(f"Set response time for chat entry {self.id}: {response_time_ms}ms")
    
    def mark_error(self, error_message: str = None) -> None:
        """Mark this entry as having an error"""
        self.error_occurred = 'Y'
        if error_message:
            current_metadata = self.get_metadata()
            current_metadata['error_message'] = error_message
            self.set_metadata(current_metadata)
        
        logger.warning(f"Marked chat entry {self.id} as having error: {error_message}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'message': self.message,
            'response': self.response,
            'message_type': self.message_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'meta_data': self.get_metadata(),
            'response_time': self.response_time,
            'error_occurred': self.error_occurred == 'Y'
        }
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<ChatHistory(id={self.id}, user_id='{self.user_id}', type='{self.message_type}', timestamp='{self.timestamp}')>"
    
    @classmethod
    def create_entry(
        cls,
        user_id: str,
        message: str,
        response: str,
        message_type: str = 'text',
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        response_time: Optional[int] = None
    ) -> 'ChatHistory':
        """Create a new chat history entry"""
        entry = cls(
            user_id=user_id,
            session_id=session_id,
            message=message,
            response=response,
            message_type=message_type
        )
        
        if metadata:
            entry.set_metadata(metadata)
        
        if response_time:
            entry.set_response_time(response_time)
        
        logger.info(f"Created chat history entry {entry.id} for user {user_id}")
        return entry
    
    @classmethod
    def get_user_history(
        cls,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        message_type: Optional[str] = None,
        include_errors: bool = False
    ) -> list:
        """Get chat history for a specific user with filtering options"""
        from sqlalchemy.orm import Session
        from sqlalchemy import select
        
        # This method would be implemented in a service layer
        # For now, it's a placeholder showing the intended interface
        logger.debug(f"Getting chat history for user {user_id}, limit: {limit}, offset: {offset}")
        
        # Placeholder implementation
        return []
    
    @classmethod
    def get_session_history(
        cls,
        session_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> list:
        """Get chat history for a specific session"""
        logger.debug(f"Getting chat history for session {session_id}, limit: {limit}, offset: {offset}")
        
        # Placeholder implementation
        return []
    
    @classmethod
    def cleanup_old_entries(
        cls,
        days_old: int = 90,
        max_entries_per_user: int = 1000
    ) -> int:
        """Clean up old chat history entries"""
        logger.info(f"Cleaning up chat history entries older than {days_old} days")
        
        # Placeholder implementation
        return 0
