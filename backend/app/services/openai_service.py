from openai import OpenAI
from ..core.config import settings

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_free_diagnosis(self, name: str, birth_date: str) -> str:
        """
        無料診断の結果を生成する
        """
        prompt = f"""
あなたは占い師です。以下の情報から、その人の運勢を占ってください:

名前: {name}
生年月日: {birth_date}

以下の項目について、簡潔に占ってください:
- 総合運
- 恋愛運
- 仕事運
- 金運

各項目2-3文程度で、具体的なアドバイスを含めてください。
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは経験豊富な占い師です。スピリチュアルな言葉を使いながら、ポジティブで具体的なアドバイスを提供してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI APIエラー: {str(e)}")

    async def generate_detailed_diagnosis(self, name: str, birth_date: str, categories: list[str], free_text: str) -> str:
        """
        有料診断の詳細な結果を生成する
        """
        prompt = f"""
名前: {name}
生年月日: {birth_date}
占いを希望する分野: {', '.join(categories)}
具体的な悩み: {free_text}

以下の内容で詳細な占い結果を生成してください:

1. 全体的な運勢の流れ
2. 選択された各分野の詳細な運勢
3. 具体的なアドバイスと行動指針
4. 開運のためのアクション
5. ラッキーアイテム・カラー

各項目について、具体的で実践的なアドバイスを含めて、詳しく説明してください。
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは経験豊富な占い師です。スピリチュアルな言葉を使いながら、ポジティブで具体的なアドバイスを提供してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI APIエラー: {str(e)}")

# サービスのグローバルインスタンス
openai_service = OpenAIService()
