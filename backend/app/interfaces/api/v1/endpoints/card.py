from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.application.card.dto import CreateCardRequest, UpdateCardRequest, CardResponse, CardListResponse
from app.application.card.service import CardService
from app.application.card.generator import CardGenerator
from app.infrastructure.repositories.card_repository import SQLAlchemyCardRepository
from app.domain.card.value_objects import CardType
from pydantic import BaseModel, Field

router = APIRouter()


class GenerateCardsRequest(BaseModel):
    """生成卡片请求DTO"""
    text: str = Field(..., description="输入文本")
    card_type: CardType = Field(CardType.BASIC, description="卡片类型")
    provider: str = Field("siliconflow", description="LLM提供商")
    max_cards: int = Field(5, ge=1, le=20, description="最大生成卡片数")
    auto_save: bool = Field(True, description="是否自动保存生成的卡片")

    class Config:
        extra = "ignore"


class GenerateCardsResponse(BaseModel):
    """生成卡片响应DTO"""
    generated_cards: List[CardResponse]
    saved_cards: List[CardResponse]
    total_generated: int
    total_saved: int

    class Config:
        extra = "ignore"


def get_card_service(db: Session = Depends(get_db)) -> CardService:
    """获取卡片服务实例"""
    repository = SQLAlchemyCardRepository(db)
    return CardService(repository)


@router.post("/cards", response_model=CardResponse)
async def create_card(
    request: CreateCardRequest,
    user_id: str = Query(..., description="用户ID"),
    card_service: CardService = Depends(get_card_service)
):
    """创建新卡片"""
    try:
        return await card_service.create_card(user_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cards/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: str,
    user_id: str = Query(..., description="用户ID"),
    card_service: CardService = Depends(get_card_service)
):
    """获取单个卡片"""
    card = await card_service.get_card(card_id, user_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/cards", response_model=CardListResponse)
async def get_cards(
    user_id: str = Query(..., description="用户ID"),
    skip: int = Query(0, ge=0, description="跳过的卡片数量"),
    limit: int = Query(100, ge=1, le=1000, description="返回的卡片数量"),
    card_service: CardService = Depends(get_card_service)
):
    """获取用户卡片列表"""
    return await card_service.get_user_cards(user_id, skip, limit)


@router.put("/cards/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: str,
    request: UpdateCardRequest,
    user_id: str = Query(..., description="用户ID"),
    card_service: CardService = Depends(get_card_service)
):
    """更新卡片"""
    try:
        card = await card_service.update_card(card_id, user_id, request)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return card
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/cards/{card_id}")
async def delete_card(
    card_id: str,
    user_id: str = Query(..., description="用户ID"),
    card_service: CardService = Depends(get_card_service)
):
    """删除卡片"""
    success = await card_service.delete_card(card_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully"}


@router.get("/cards/search", response_model=CardListResponse)
async def search_cards(
    user_id: str = Query(..., description="用户ID"),
    q: str = Query(..., description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过的卡片数量"),
    limit: int = Query(100, ge=1, le=1000, description="返回的卡片数量"),
    card_service: CardService = Depends(get_card_service)
):
    """搜索卡片"""
    return await card_service.search_cards(user_id, q, skip, limit)


@router.get("/cards/by-tags", response_model=CardListResponse)
async def get_cards_by_tags(
    user_id: str = Query(..., description="用户ID"),
    tags: str = Query(..., description="标签列表，用逗号分隔"),
    skip: int = Query(0, ge=0, description="跳过的卡片数量"),
    limit: int = Query(100, ge=1, le=1000, description="返回的卡片数量"),
    card_service: CardService = Depends(get_card_service)
):
    """根据标签获取卡片"""
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    return await card_service.get_cards_by_tags(user_id, tag_list, skip, limit)


@router.post("/cards/generate", response_model=GenerateCardsResponse)
async def generate_cards(
    request: GenerateCardsRequest,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """从文本生成卡片"""
    try:
        # 创建卡片生成器
        generator = CardGenerator()

        # 生成卡片
        generated_cards = await generator.generate_cards_from_text(
            text=request.text,
            user_id=user_id,
            card_type=request.card_type,
            provider=request.provider,
            max_cards=request.max_cards
        )

        # 转换为响应格式
        generated_responses = []
        saved_responses = []

        # 如果需要自动保存
        if request.auto_save:
            card_service = get_card_service(db)

            for card in generated_cards:
                try:
                    saved_card = await card_service.create_card(user_id, CreateCardRequest(
                        title=card.title,
                        card_type=card.card_type,
                        content=card.content.dict(),
                        tags=card.tags
                    ))
                    saved_responses.append(saved_card)
                except Exception as e:
                    print(f"保存卡片失败: {e}")
                    continue
        else:
            # 不自动保存，只返回生成的卡片
            for card in generated_cards:
                generated_responses.append(CardResponse(
                    id=card.id,
                    user_id=card.user_id,
                    title=card.title,
                    card_type=card.card_type,
                    content=card.content.dict(),
                    tags=card.tags,
                    created_at=card.created_at.isoformat(),
                    updated_at=card.updated_at.isoformat()
                ))

        return GenerateCardsResponse(
            generated_cards=generated_responses if not request.auto_save else saved_responses,
            saved_cards=saved_responses,
            total_generated=len(generated_cards),
            total_saved=len(saved_responses)
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"生成卡片失败: {str(e)}")