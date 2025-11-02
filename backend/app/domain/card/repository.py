from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import Card


class CardRepository(ABC):
    """卡片仓储接口"""

    @abstractmethod
    async def create(self, card: Card) -> Card:
        """创建卡片"""
        pass

    @abstractmethod
    async def get_by_id(self, card_id: str, user_id: str) -> Optional[Card]:
        """根据ID获取卡片（确保用户隔离）"""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Card]:
        """获取用户的所有卡片"""
        pass

    @abstractmethod
    async def update(self, card: Card) -> Card:
        """更新卡片"""
        pass

    @abstractmethod
    async def delete(self, card_id: str, user_id: str) -> bool:
        """删除卡片"""
        pass

    @abstractmethod
    async def count_by_user(self, user_id: str) -> int:
        """统计用户卡片总数"""
        pass

    @abstractmethod
    async def search(self, user_id: str, query: str, skip: int = 0, limit: int = 100) -> List[Card]:
        """搜索用户卡片"""
        pass

    @abstractmethod
    async def get_by_tags(self, user_id: str, tags: List[str], skip: int = 0, limit: int = 100) -> List[Card]:
        """根据标签获取用户卡片"""
        pass