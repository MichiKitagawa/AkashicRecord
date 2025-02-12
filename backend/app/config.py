# /app/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict  # pydantic からインポートする

class Settings(BaseSettings):
    # 基本的なアプリケーション設定
    OPENAI_API_KEY: str
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:3000"

    model_config: ConfigDict = {
         "env_file": ".env",           # .env ファイルから環境変数を読み込む
         "extra": "allow",             # 未定義の環境変数も許容する
         "case_sensitive": True,       # 大文字小文字を区別する
    }

settings = Settings()
