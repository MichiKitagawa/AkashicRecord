from openai import OpenAI
from ..errors import OpenAIError
from ..config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class OpenAIService:
    def __init__(self):
        pass

    async def generate_free_diagnosis(self, name: str, birth_date: str) -> str:
        """
        無料診断の結果を生成する
        """
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは占い師です。"},
                    {"role": "user", "content": f"名前: {name}\n生年月日: {birth_date}\nこの情報から運勢を占ってください。"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise OpenAIError(str(e))

    async def generate_detailed_diagnosis(
        self,
        name: str,
        birth_date: str,
        categories: list[str],
        free_text: str = ""
    ) -> str:
        """
        有料診断の詳細な結果を生成する
        """
        try:
            category_text = "、".join(categories)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは占い師です。"},
                    {"role": "user", "content": f"名前: {name}\n生年月日: {birth_date}\n占いたい項目: {category_text}\n具体的な相談内容: {free_text}\n\nそれぞれの項目について詳しく占ってください。"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise OpenAIError(str(e))

# サービスのグローバルインスタンス
openai_service = OpenAIService()
