from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from .value_objects import CardType, CardContent, CardContentFactory


class Card:
    """卡片实体"""

    def __init__(
        self,
        user_id: str,
        title: str,
        card_type: CardType,
        content: CardContent,
        tags: Optional[list[str]] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid4())
        self.user_id = user_id
        self.title = title
        self.card_type = card_type
        self.content = content
        self.tags = tags or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_content(self, content: CardContent) -> None:
        """更新卡片内容"""
        self.content = content
        self.updated_at = datetime.utcnow()

    def update_title(self, title: str) -> None:
        """更新卡片标题"""
        self.title = title
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str) -> None:
        """添加标签"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def remove_tag(self, tag: str) -> None:
        """移除标签"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()

    def is_owned_by(self, user_id: str) -> bool:
        """检查卡片是否属于指定用户"""
        return self.user_id == user_id

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "card_type": self.card_type.value,
            "content": self.content.dict(),
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Card":
        """从字典创建卡片"""
        content = CardContentFactory.create_content(
            CardType(data["card_type"]),
            **data["content"]
        )

        return cls(
            user_id=data["user_id"],
            title=data["title"],
            card_type=CardType(data["card_type"]),
            content=content,
            tags=data.get("tags", []),
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )