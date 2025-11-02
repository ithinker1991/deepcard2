from typing import List, Optional
from pydantic import BaseModel, Field

from app.domain.card.value_objects import CardType


class CreateCardRequest(BaseModel):
    """创建卡片请求DTO"""
    title: str = Field(..., description="卡片标题")
    card_type: CardType = Field(..., description="卡片类型")
    content: dict = Field(..., description="卡片内容")
    tags: Optional[List[str]] = Field(default_factory=list, description="标签")

    class Config:
        extra = "ignore"


class UpdateCardRequest(BaseModel):
    """更新卡片请求DTO"""
    title: Optional[str] = Field(None, description="卡片标题")
    content: Optional[dict] = Field(None, description="卡片内容")
    tags: Optional[List[str]] = Field(None, description="标签")

    class Config:
        extra = "ignore"


class CardResponse(BaseModel):
    """卡片响应DTO"""
    id: str
    user_id: str
    title: str
    card_type: CardType
    content: dict
    tags: List[str]
    created_at: str
    updated_at: str

    class Config:
        extra = "ignore"


class CardListResponse(BaseModel):
    """卡片列表响应DTO"""
    cards: List[CardResponse]
    total: int
    skip: int
    limit: int

    class Config:
        extra = "ignore"