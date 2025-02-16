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
        if not token:
            logger.error("診断トークンが指定されていません")
            raise DiagnosisError("診断トークンが指定されていません")

        try:
            logger.debug(f"診断結果の取得を開始します。token: {token}")
            
            # ドキュメントの参照を取得
            doc_ref = self.collection.document(token)
            
            # 非同期でFirebaseの操作を実行
            doc = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: doc_ref.get()
            )
            
            if not doc.exists:
                logger.error(f"診断結果が見つかりません。token: {token}")
                raise DiagnosisError("指定された診断結果が見つかりません")
            
            result = doc.to_dict()
            if not result:
                logger.error(f"診断結果のデータが不正です。token: {token}")
                raise DiagnosisError("診断結果のデータが不正です")
                
            logger.debug(f"診断結果を取得しました。token: {token}")
            return result
            
        except google_exceptions.PermissionDenied as e:
            logger.error(f"Firestore APIへのアクセス権限がありません: {str(e)}")
            raise DiagnosisError("データベースへのアクセス権限がありません。管理者に連絡してください。")
            
        except google_exceptions.NotFound as e:
            logger.error(f"Firestoreのドキュメントが見つかりません: {str(e)}")
            raise DiagnosisError("指定された診断結果が見つかりません")
            
        except asyncio.CancelledError:
            logger.error(f"診断結果の取得がキャンセルされました。token: {token}")
            raise DiagnosisError("診断結果の取得がキャンセルされました")
            
        except Exception as e:
            logger.error(f"診断結果の取得中に予期せぬエラーが発生しました: {str(e)}")
            raise DiagnosisError(f"診断結果の取得に失敗しました: {str(e)}")

    async def unlock_diagnosis(self, token: str) -> None:
        """
        診断結果のロックを解除する
        """
        if not token:
            logger.error("診断トークンが指定されていません")
            raise DiagnosisError("診断トークンが指定されていません")

        try:
            logger.debug(f"診断結果のロック解除を開始します。token: {token}")
            
            # ドキュメントの参照を取得
            doc_ref = self.collection.document(token)
            
            # ドキュメントの存在確認
            doc = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: doc_ref.get()
            )
            
            if not doc.exists:
                logger.error(f"診断結果が見つかりません。token: {token}")
                raise DiagnosisError("指定された診断結果が見つかりません")
                
            # 現在のデータを取得
            current_data = doc.to_dict()
            if not current_data:
                logger.error(f"診断結果のデータが不正です。token: {token}")
                raise DiagnosisError("診断結果のデータが不正です")
                
            # すでにロック解除されている場合は早期リターン
            if current_data.get('is_unlocked'):
                logger.debug(f"診断結果はすでにロック解除されています。token: {token}")
                return
                
            # ロック解除を実行
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: doc_ref.update({
                    'is_unlocked': True,
                    'updated_at': datetime.utcnow()
                })
            )
            
            logger.debug(f"診断結果のロック解除が完了しました。token: {token}")
            
        except google_exceptions.PermissionDenied as e:
            logger.error(f"Firestore APIへのアクセス権限がありません: {str(e)}")
            raise DiagnosisError("データベースへのアクセス権限がありません。管理者に連絡してください。")
            
        except google_exceptions.NotFound as e:
            logger.error(f"Firestoreのドキュメントが見つかりません: {str(e)}")
            raise DiagnosisError("指定された診断結果が見つかりません")
            
        except asyncio.CancelledError:
            logger.error(f"診断結果のロック解除がキャンセルされました。token: {token}")
            raise DiagnosisError("診断結果のロック解除がキャンセルされました")
            
        except Exception as e:
            logger.error(f"診断結果のロック解除中に予期せぬエラーが発生しました: {str(e)}")
            raise DiagnosisError(f"診断結果のロック解除に失敗しました: {str(e)}")

diagnosis_store = DiagnosisStore() 