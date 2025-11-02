"""
SiliconFlow LLM provider implementation.
"""
from typing import Dict, Any
import httpx

from app.infrastructure.llm.base import LLMProvider, LLMConnectionError, LLMGenerationError


class SiliconFlowProvider(LLMProvider):
    """SiliconFlow API provider."""

    def __init__(self, api_key: str, model: str = "deepseek-ai/DeepSeek-V3", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = kwargs.get('base_url', 'https://api.siliconflow.cn/v1')
        self.max_tokens = kwargs.get('max_tokens', 1000)
        self.temperature = kwargs.get('temperature', 0.7)

    @property
    def provider_name(self) -> str:
        return "siliconflow"

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using SiliconFlow API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": kwargs.get('model', self.model),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get('max_tokens', self.max_tokens),
            "temperature": kwargs.get('temperature', self.temperature)
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise LLMConnectionError(f"Invalid API key for SiliconFlow: {e}")
            elif e.response.status_code == 429:
                raise LLMConnectionError(f"Rate limit exceeded for SiliconFlow: {e}")
            else:
                raise LLMGenerationError(f"SiliconFlow API error: {e}")
        except httpx.RequestError as e:
            raise LLMConnectionError(f"Connection error with SiliconFlow: {e}")
        except (KeyError, IndexError) as e:
            raise LLMGenerationError(f"Invalid response format from SiliconFlow: {e}")

    async def test_connection(self) -> Dict[str, Any]:
        """Test SiliconFlow API connection."""
        try:
            test_prompt = "Say 'Hello, SiliconFlow!'"
            response = await self.generate_text(test_prompt)

            return {
                "status": "success",
                "provider": self.provider_name,
                "model": self.model,
                "test_response": response[:100],  # Limit response length
                "message": "Connection successful"
            }
        except Exception as e:
            return {
                "status": "error",
                "provider": self.provider_name,
                "model": self.model,
                "error": str(e),
                "message": "Connection failed"
            }