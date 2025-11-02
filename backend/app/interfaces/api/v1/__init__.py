"""
API v1 router.
"""
from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import llm

api_router = APIRouter()

api_router.include_router(llm.router, prefix="/llm", tags=["llm"])