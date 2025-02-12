import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# .env をロード
load_dotenv()

# 環境変数から JSON キーファイルのパスを取得
firebase_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not firebase_key_path:
    raise ValueError("環境変数 'GOOGLE_APPLICATION_CREDENTIALS' が設定されていません。")

# Firebase Admin SDKの初期化
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Firestoreクライアントの初期化
db = firestore.client()
