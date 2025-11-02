from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, JSON
from sqlalchemy.orm import relationship

from app.shared.database import Base


class Card(Base):
    """卡片SQLAlchemy模型"""
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    class Config:
        extra = "ignore"