from datetime import datetime
from ..core.firebase import db
from ..errors import DiagnosisError

class DiagnosisStore:
    def __init__(self):
        self.collection = db.collection('diagnoses')

    async def create_diagnosis(
        self,
        name: str,
        birth_date: str,
        result: str,
        categories: list[str] = None,
        free_text: str = None,
        is_detailed: bool = False
    ) -> str:
        """
        診断結果を保存し、診断トークンを返す
        """
        try:
            doc_ref = self.collection.document()
            doc_ref.set({
                'name': name,
                'birth_date': birth_date,
                'result': result,
                'categories': categories or [],
                'free_text': free_text or '',
                'is_detailed': is_detailed,
                'is_unlocked': not is_detailed,  # 無料診断の場合はすぐにアンロック
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
            return doc_ref.id
        except Exception as e:
            raise DiagnosisError(f"診断結果の保存に失敗しました: {str(e)}")

    async def get_diagnosis(self, token: str) -> dict:
        """
        診断結果を取得する
        """
        try:
            doc = self.collection.document(token).get()
            if not doc.exists:
                raise DiagnosisError("指定された診断結果が見つかりません")
            return doc.to_dict()
        except Exception as e:
            raise DiagnosisError(f"診断結果の取得に失敗しました: {str(e)}")

    async def unlock_diagnosis(self, token: str) -> None:
        """
        診断結果のロックを解除する
        """
        try:
            doc_ref = self.collection.document(token)
            doc_ref.update({
                'is_unlocked': True,
                'updated_at': datetime.utcnow()
            })
        except Exception as e:
            raise DiagnosisError(f"診断結果のロック解除に失敗しました: {str(e)}")

diagnosis_store = DiagnosisStore() 