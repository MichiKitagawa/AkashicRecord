import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .envファイルの読み込み
load_dotenv()

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "Akashic AI Divination API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # OpenAI API設定
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Stripe API設定
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # データベース設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        case_sensitive = True

# グローバル設定インスタンス
settings = Settings()
