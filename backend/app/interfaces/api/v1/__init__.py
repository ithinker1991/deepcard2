"""
API v1 router.
"""
from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import llm, card

api_router = APIRouter()

api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(card.router, tags=["cards"])