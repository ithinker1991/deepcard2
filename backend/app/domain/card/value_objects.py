from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CardType(str, Enum):
    """卡片类型枚举"""
    BASIC = "basic"          # 基础卡片：正面问题，背面答案
    cloze = "cloze"          # 填空题：带空格的文本
    QNA = "qna"              # 问答对：多轮问答
    CONCEPT = "concept"      # 概念卡：概念定义+例子


class CardContent(BaseModel):
    """卡片内容值对象"""
    front: str = Field(..., description="卡片正面内容")
    back: str = Field(..., description="卡片背面内容")

    class Config:
        extra = "ignore"


class ClozeContent(CardContent):
    """填空题内容"""
    cloze_text: str = Field(..., description="带空格的文本")
    cloze_answer: str = Field(..., description="空格答案")


class QnAContent(CardContent):
    """问答对内容"""
    question: str = Field(..., description="问题")
    answer: str = Field(..., description="答案")
    follow_up: Optional[Dict[str, Any]] = Field(None, description="追问和回答")


class ConceptContent(CardContent):
    """概念卡片内容"""
    concept: str = Field(..., description="概念名称")
    definition: str = Field(..., description="概念定义")
    examples: list[str] = Field(default_factory=list, description="示例")


class CardContentFactory:
    """卡片内容工厂"""

    @staticmethod
    def create_content(card_type: CardType, **kwargs) -> CardContent:
        """根据卡片类型创建内容"""
        if card_type == CardType.BASIC:
            return CardContent(**kwargs)
        elif card_type == CardType.cloze:
            return ClozeContent(**kwargs)
        elif card_type == CardType.QNA:
            return QnAContent(**kwargs)
        elif card_type == CardType.CONCEPT:
            return ConceptContent(**kwargs)
        else:
            raise ValueError(f"Unsupported card type: {card_type}")