from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.domain.card.entity import Card
from app.domain.card.repository import CardRepository
from app.domain.card.value_objects import CardContentFactory, CardType
from app.infrastructure.database.models import Card as CardModel


class SQLAlchemyCardRepository(CardRepository):
    """基于SQLAlchemy的卡片仓储实现"""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, card: Card) -> Card:
        """创建卡片"""
        db_card = CardModel(
            id=card.id,
            user_id=card.user_id,
            title=card.title,
            card_type=card.card_type.value,
            content=card.content.dict(),
            tags=card.tags,
            created_at=card.created_at,
            updated_at=card.updated_at,
        )

        self.db.add(db_card)
        self.db.commit()
        self.db.refresh(db_card)

        return self._model_to_entity(db_card)

    async def get_by_id(self, card_id: str, user_id: str) -> Optional[Card]:
        """根据ID获取卡片（确保用户隔离）"""
        db_card = self.db.query(CardModel).filter(
            and_(CardModel.id == card_id, CardModel.user_id == user_id)
        ).first()

        if not db_card:
            return None

        return self._model_to_entity(db_card)

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Card]:
        """获取用户的所有卡片"""
        db_cards = self.db.query(CardModel).filter(
            CardModel.user_id == user_id
        ).offset(skip).limit(limit).all()

        return [self._model_to_entity(card) for card in db_cards]

    async def update(self, card: Card) -> Card:
        """更新卡片"""
        db_card = self.db.query(CardModel).filter(
            and_(CardModel.id == card.id, CardModel.user_id == card.user_id)
        ).first()

        if not db_card:
            raise ValueError(f"Card {card.id} not found for user {card.user_id}")

        db_card.title = card.title
        db_card.content = card.content.dict()
        db_card.tags = card.tags
        db_card.updated_at = card.updated_at

        self.db.commit()
        self.db.refresh(db_card)

        return self._model_to_entity(db_card)

    async def delete(self, card_id: str, user_id: str) -> bool:
        """删除卡片"""
        db_card = self.db.query(CardModel).filter(
            and_(CardModel.id == card_id, CardModel.user_id == user_id)
        ).first()

        if not db_card:
            return False

        self.db.delete(db_card)
        self.db.commit()

        return True

    async def count_by_user(self, user_id: str) -> int:
        """统计用户卡片总数"""
        return self.db.query(CardModel).filter(
            CardModel.user_id == user_id
        ).count()

    async def search(self, user_id: str, query: str, skip: int = 0, limit: int = 100) -> List[Card]:
        """搜索用户卡片"""
        db_cards = self.db.query(CardModel).filter(
            and_(
                CardModel.user_id == user_id,
                or_(
                    CardModel.title.contains(query),
                    CardModel.content["front"].astext.contains(query),
                    CardModel.content["back"].astext.contains(query)
                )
            )
        ).offset(skip).limit(limit).all()

        return [self._model_to_entity(card) for card in db_cards]

    async def get_by_tags(self, user_id: str, tags: List[str], skip: int = 0, limit: int = 100) -> List[Card]:
        """根据标签获取用户卡片"""
        db_cards = self.db.query(CardModel).filter(
            and_(
                CardModel.user_id == user_id,
                CardModel.tags.overlap(tags)
            )
        ).offset(skip).limit(limit).all()

        return [self._model_to_entity(card) for card in db_cards]

    def _model_to_entity(self, db_card: CardModel) -> Card:
        """将数据库模型转换为领域实体"""
        content = CardContentFactory.create_content(
            CardType(db_card.card_type),
            **db_card.content
        )

        return Card(
            id=db_card.id,
            user_id=db_card.user_id,
            title=db_card.title,
            card_type=CardType(db_card.card_type),
            content=content,
            tags=db_card.tags or [],
            created_at=db_card.created_at,
            updated_at=db_card.updated_at,
        )