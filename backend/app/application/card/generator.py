"""卡片生成服务"""

from typing import List, Dict, Any
from app.infrastructure.llm.factory import LLMFactory
from app.domain.card.entity import Card
from app.domain.card.value_objects import CardType, CardContentFactory
from app.shared.config import get_settings


class CardGenerator:
    """卡片生成器"""

    def __init__(self):
        self.settings = get_settings()

    async def generate_cards_from_text(
        self,
        text: str,
        user_id: str,
        card_type: CardType = CardType.BASIC,
        provider: str = "siliconflow",
        max_cards: int = 5
    ) -> List[Card]:
        """从文本生成卡片"""

        # 获取API密钥
        api_key = self._get_api_key(provider)

        # 获取模型配置
        model_config = LLMFactory.get_provider_models(provider)
        model = model_config.get("default")

        # 获取LLM提供商
        llm_provider = LLMFactory.create_provider(provider, api_key=api_key, model=model)

        # 根据卡片类型生成提示词
        prompt = self._build_generation_prompt(text, card_type, max_cards)

        # 调用LLM生成卡片内容
        response_text = await llm_provider.generate_text(prompt)

        # 解析生成的卡片内容
        generated_cards = self._parse_generated_cards(
            response_text,
            user_id,
            card_type
        )

        return generated_cards

    def _build_generation_prompt(self, text: str, card_type: CardType, max_cards: int) -> str:
        """构建生成提示词"""

        if card_type == CardType.BASIC:
            prompt = f"""
请根据以下文本，生成最多{max_cards}张学习卡片。每张卡片包含一个问题和一个答案。

文本内容：
{text}

请按以下JSON格式返回：
{{
    "cards": [
        {{
            "title": "卡片标题",
            "content": {{
                "front": "问题",
                "back": "答案"
            }},
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

注意：
1. 问题应该基于文本中的重要概念
2. 答案要准确、简洁
3. 标签要反映卡片的主要内容
4. 严格按JSON格式返回
"""
        elif card_type == CardType.cloze:
            prompt = f"""
请根据以下文本，生成最多{max_cards}张填空题卡片。

文本内容：
{text}

请按以下JSON格式返回：
{{
    "cards": [
        {{
            "title": "卡片标题",
            "content": {{
                "front": "填空题",
                "back": "答案",
                "cloze_text": "带{{空格}}的文本",
                "cloze_answer": "空格的答案"
            }},
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

注意：
1. 选择文本中的关键信息作为空格
2. 空格应该测试对重要概念的理解
3. 严格按JSON格式返回
"""
        elif card_type == CardType.QNA:
            prompt = f"""
请根据以下文本，生成最多{max_cards}张问答对卡片。

文本内容：
{text}

请按以下JSON格式返回：
{{
    "cards": [
        {{
            "title": "卡片标题",
            "content": {{
                "front": "问答对",
                "back": "问答对",
                "question": "问题",
                "answer": "答案"
            }},
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

注意：
1. 问题应该覆盖文本的核心内容
2. 答案要全面且准确
3. 严格按JSON格式返回
"""
        elif card_type == CardType.CONCEPT:
            prompt = f"""
请根据以下文本，生成最多{max_cards}张概念卡片。

文本内容：
{text}

请按以下JSON格式返回：
{{
    "cards": [
        {{
            "title": "卡片标题",
            "content": {{
                "front": "概念",
                "back": "概念",
                "concept": "概念名称",
                "definition": "概念定义",
                "examples": ["示例1", "示例2"]
            }},
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

注意：
1. 识别文本中的重要概念
2. 提供清晰的定义和具体的例子
3. 严格按JSON格式返回
"""
        else:
            raise ValueError(f"Unsupported card type: {card_type}")

        return prompt

    def _parse_generated_cards(
        self,
        response_text: str,
        user_id: str,
        card_type: CardType
    ) -> List[Card]:
        """解析生成的卡片内容"""

        import json
        import re

        try:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
            else:
                data = json.loads(response_text)

            cards = []
            for card_data in data.get("cards", []):
                try:
                    # 创建内容对象
                    content = CardContentFactory.create_content(
                        card_type,
                        **card_data["content"]
                    )

                    # 创建卡片实体
                    card = Card(
                        user_id=user_id,
                        title=card_data["title"],
                        card_type=card_type,
                        content=content,
                        tags=card_data.get("tags", [])
                    )

                    cards.append(card)

                except Exception as e:
                    # 跳过无法解析的卡片
                    print(f"跳过无效卡片: {e}")
                    continue

            return cards

        except Exception as e:
            raise ValueError(f"解析生成内容失败: {e}")

    def _get_api_key(self, provider: str) -> str:
        """获取LLM提供商的API密钥"""
        provider_keys = {
            "openai": self.settings.OPENAI_API_KEY,
            "deepseek": self.settings.DEEPSEEK_API_KEY,
            "siliconflow": self.settings.SILICONFLOW_API_KEY,
        }

        api_key = provider_keys.get(provider)
        if not api_key:
            raise ValueError(f"API key not found for provider: {provider}")

        return api_key