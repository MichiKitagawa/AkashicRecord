import aiohttp
import json
from ..core.config import settings
from ..errors import OpenAIError
import logging

logger = logging.getLogger(__name__)

class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.FRONTEND_URL,
            "Content-Type": "application/json"
        }

    async def _generate_completion(self, messages: list) -> str:
        """
        OpenRouter APIを使用して回答を生成する
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": "anthropic/claude-3-haiku",
                        "messages": messages
                    }
                ) as response:
                    if response.status != 200:
                        error_detail = await response.text()
                        logger.error(f"OpenRouter API error: {error_detail}")
                        raise OpenAIError(f"OpenRouter API error: {error_detail}")

                    result = await response.json()
                    return result['choices'][0]['message']['content']

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            raise OpenAIError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise OpenAIError(f"Error generating completion: {str(e)}")

    async def generate_free_diagnosis(self, name: str, birth_date: str) -> str:
        """
        無料診断の結果を生成する
        """
        try:
            messages = [
                {"role": "system", "content": "あなたはアカシックレコードを読み取ることができる占い師です。"},
                {"role": "user", "content": f"名前: {name}\n生年月日: {birth_date}\n\nこの人の運勢を簡潔に占ってください。"}
            ]
            return await self._generate_completion(messages)
        except Exception as e:
            logger.error(f"Error in generate_free_diagnosis: {str(e)}")
            raise OpenAIError(str(e))

    async def generate_detailed_diagnosis(
        self,
        name: str,
        birth_date: str,
        categories: list[str],
        free_text: str = ""
    ) -> str:
        """
        詳細な診断結果を生成する
        """
        try:
            category_text = "\n".join([f"- {category}" for category in categories])
            messages = [
                {"role": "system", "content": "あなたはアカシックレコードを読み取ることができる占い師です。詳細な鑑定を行ってください。"},
                {"role": "user", "content": f"""
名前: {name}
生年月日: {birth_date}

鑑定を希望する項目:
{category_text}

補足情報:
{free_text}

上記の情報に基づいて、詳細な鑑定結果を提供してください。
各項目について具体的なアドバイスも含めてください。"""}
            ]
            return await self._generate_completion(messages)
        except Exception as e:
            logger.error(f"Error in generate_detailed_diagnosis: {str(e)}")
            raise OpenAIError(str(e))

openai_service = OpenRouterService()
