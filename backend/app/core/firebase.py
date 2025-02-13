import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import logging
from google.api_core import exceptions as google_exceptions

# ロガーの設定
logger = logging.getLogger(__name__)

# .env をロード
load_dotenv()

# 環境変数から JSON キーファイルのパスを取得
firebase_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not firebase_key_path:
    raise ValueError("環境変数 'GOOGLE_APPLICATION_CREDENTIALS' が設定されていません。")

try:
    logger.debug(f"Firebaseの初期化を開始します。キーファイル: {firebase_key_path}")
    
    # Firebase Admin SDKの初期化
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        logger.debug("Firebase Admin SDKの初期化が完了しました。")
    
    # Firestoreクライアントの初期化
    db = firestore.client()
    logger.debug("Firestoreクライアントの初期化が完了しました。")
    
except google_exceptions.PermissionDenied as e:
    logger.error(f"Firestore APIへのアクセス権限がありません: {str(e)}")
    logger.error("Firestore APIを有効化してください: https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=akashirecord-10950")
    raise
except Exception as e:
    logger.error(f"Firebaseの初期化中にエラーが発生しました: {str(e)}")
    raise
