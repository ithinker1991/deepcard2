from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.card.entity import Card
from app.domain.card.repository import CardRepository
from app.domain.card.value_objects import CardContentFactory, CardType
from app.application.card.dto import CreateCardRequest, UpdateCardRequest, CardResponse, CardListResponse


class CardService:
    """卡片应用服务"""

    def __init__(self, card_repository: CardRepository):
        self.card_repository = card_repository

    async def create_card(self, user_id: str, request: CreateCardRequest) -> CardResponse:
        """创建卡片"""
        content = CardContentFactory.create_content(
            request.card_type,
            **request.content
        )

        card = Card(
            user_id=user_id,
            title=request.title,
            card_type=request.card_type,
            content=content,
            tags=request.tags or []
        )

        created_card = await self.card_repository.create(card)
        return self._entity_to_response(created_card)

    async def get_card(self, card_id: str, user_id: str) -> Optional[CardResponse]:
        """获取单个卡片"""
        card = await self.card_repository.get_by_id(card_id, user_id)
        if not card:
            return None
        return self._entity_to_response(card)

    async def get_user_cards(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> CardListResponse:
        """获取用户卡片列表"""
        cards = await self.card_repository.get_by_user(user_id, skip, limit)
        total = await self.card_repository.count_by_user(user_id)

        card_responses = [self._entity_to_response(card) for card in cards]
        return CardListResponse(
            cards=card_responses,
            total=total,
            skip=skip,
            limit=limit
        )

    async def update_card(
        self,
        card_id: str,
        user_id: str,
        request: UpdateCardRequest
    ) -> Optional[CardResponse]:
        """更新卡片"""
        card = await self.card_repository.get_by_id(card_id, user_id)
        if not card:
            return None

        # 更新标题
        if request.title is not None:
            card.update_title(request.title)

        # 更新内容
        if request.content is not None:
            content = CardContentFactory.create_content(
                card.card_type,
                **request.content
            )
            card.update_content(content)

        # 更新标签
        if request.tags is not None:
            card.tags = request.tags
            card.updated_at = card.updated_at  # 触发更新时间

        updated_card = await self.card_repository.update(card)
        return self._entity_to_response(updated_card)

    async def delete_card(self, card_id: str, user_id: str) -> bool:
        """删除卡片"""
        return await self.card_repository.delete(card_id, user_id)

    async def search_cards(
        self,
        user_id: str,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> CardListResponse:
        """搜索卡片"""
        cards = await self.card_repository.search(user_id, query, skip, limit)
        total = len(cards)  # 简化实现，实际应该有专门的count方法

        card_responses = [self._entity_to_response(card) for card in cards]
        return CardListResponse(
            cards=card_responses,
            total=total,
            skip=skip,
            limit=limit
        )

    async def get_cards_by_tags(
        self,
        user_id: str,
        tags: List[str],
        skip: int = 0,
        limit: int = 100
    ) -> CardListResponse:
        """根据标签获取卡片"""
        cards = await self.card_repository.get_by_tags(user_id, tags, skip, limit)
        total = len(cards)  # 简化实现，实际应该有专门的count方法

        card_responses = [self._entity_to_response(card) for card in cards]
        return CardListResponse(
            cards=card_responses,
            total=total,
            skip=skip,
            limit=limit
        )

    def _entity_to_response(self, card: Card) -> CardResponse:
        """将领域实体转换为响应DTO"""
        return CardResponse(
            id=card.id,
            user_id=card.user_id,
            title=card.title,
            card_type=card.card_type,
            content=card.content.dict(),
            tags=card.tags,
            created_at=card.created_at.isoformat(),
            updated_at=card.updated_at.isoformat()
        )