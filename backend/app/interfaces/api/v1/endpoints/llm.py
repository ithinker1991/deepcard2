"""
LLM-related API endpoints.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status

from app.shared.config import get_settings
from app.infrastructure.llm import LLMFactory, LLMConfigurationError, LLMConnectionError

router = APIRouter()
settings = get_settings()


@router.get("/providers", response_model=Dict[str, Any])
async def get_llm_providers():
    """Get list of supported LLM providers."""
    try:
        supported_providers = LLMFactory.get_supported_providers()
        provider_details = {}

        for provider in supported_providers:
            provider_details[provider] = LLMFactory.get_provider_models(provider)

        return {
            "providers": supported_providers,
            "details": provider_details,
            "default_provider": settings.DEFAULT_LLM_PROVIDER
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get providers: {str(e)}"
        )


@router.post("/test", response_model=Dict[str, Any])
async def test_llm_connection(request_data: Dict[str, Any]):
    """Test connection to an LLM provider."""
    try:
        provider_name = request_data.get("provider")
        api_key = request_data.get("api_key")
        model = request_data.get("model")

        if not provider_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider name is required"
            )

        # Get API key from request or settings
        if not api_key:
            if provider_name == "openai":
                api_key = settings.OPENAI_API_KEY
            elif provider_name == "deepseek":
                api_key = settings.DEEPSEEK_API_KEY
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="API key is required for this provider"
                )

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API key is required"
            )

        # Create provider and test connection
        provider = LLMFactory.create_provider(
            provider_name=provider_name,
            api_key=api_key,
            model=model,
            timeout=settings.LLM_TIMEOUT,
            max_retries=settings.LLM_MAX_RETRIES
        )

        result = await provider.test_connection()
        return result

    except LLMConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Connection test failed: {str(e)}"
        )


@router.post("/generate", response_model=Dict[str, Any])
async def generate_text(request_data: Dict[str, Any]):
    """Generate text using an LLM provider."""
    try:
        provider_name = request_data.get("provider", settings.DEFAULT_LLM_PROVIDER)
        prompt = request_data.get("prompt")
        api_key = request_data.get("api_key")
        model = request_data.get("model")

        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt is required"
            )

        # Get API key from request or settings
        if not api_key:
            if provider_name == "openai":
                api_key = settings.OPENAI_API_KEY
                model = model or settings.OPENAI_MODEL
            elif provider_name == "deepseek":
                api_key = settings.DEEPSEEK_API_KEY
                model = model or settings.DEEPSEEK_MODEL
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="API key is required for this provider"
                )

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API key is required"
            )

        # Create provider and generate text
        provider = LLMFactory.create_provider(
            provider_name=provider_name,
            api_key=api_key,
            model=model,
            timeout=settings.LLM_TIMEOUT,
            max_retries=settings.LLM_MAX_RETRIES
        )

        # Extract generation parameters
        generation_params = {
            k: v for k, v in request_data.items()
            if k in ["max_tokens", "temperature"] and v is not None
        }

        generated_text = await provider.generate_with_retry(prompt, **generation_params)

        return {
            "text": generated_text,
            "provider": provider_name,
            "model": provider.model,
            "prompt": prompt,
            "parameters": generation_params
        }

    except LLMConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except LLMConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM connection error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text generation failed: {str(e)}"
        )