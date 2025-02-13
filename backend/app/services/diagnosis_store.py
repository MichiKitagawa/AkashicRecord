from datetime import datetime
from ..core.firebase import db
from ..errors import DiagnosisError
import asyncio
import logging
from google.api_core import exceptions as google_exceptions

# ロガーの設定
logger = logging.getLogger(__name__)

class DiagnosisStore:
    def __init__(self):
        try:
            self.collection = db.collection('diagnoses')
            logger.debug("診断結果コレクションの初期化が完了しました")
        except Exception as e:
            logger.error(f"診断結果コレクションの初期化に失敗しました: {str(e)}")
            raise DiagnosisError(f"データベースの初期化に失敗しました: {str(e)}")

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
            logger.debug(f"診断結果の保存を開始します: {name}")
            doc_ref = self.collection.document()
            
            data = {
                'name': name,
                'birth_date': birth_date,
                'result': result,
                'categories': categories or [],
                'free_text': free_text or '',
                'is_detailed': is_detailed,
                'is_unlocked': not is_detailed,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            logger.debug(f"保存するデータを準備しました: {data}")
            
            try:
                # 非同期でFirebaseの操作を実行
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: doc_ref.set(data)
                )
                logger.debug(f"診断結果を保存しました。ID: {doc_ref.id}")
                return doc_ref.id
                
            except google_exceptions.PermissionDenied as e:
                logger.error(f"Firestore APIへのアクセス権限がありません: {str(e)}")
                raise DiagnosisError("データベースへのアクセス権限がありません。管理者に連絡してください。")
                
            except google_exceptions.NotFound as e:
                logger.error(f"Firestoreのコレクションが見つかりません: {str(e)}")
                raise DiagnosisError("データベースの設定が正しくありません。管理者に連絡してください。")
                
            except Exception as e:
                logger.error(f"診断結果の保存中に予期せぬエラーが発生しました: {str(e)}")
                raise DiagnosisError(f"診断結果の保存に失敗しました: {str(e)}")
                
        except Exception as e:
            logger.error(f"診断結果の保存処理全体でエラーが発生しました: {str(e)}")
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