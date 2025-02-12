# /app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field  # ConfigDict を pydantic から、Field も同様に

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "Akashic AI Divination API"
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # OpenAI API設定
    OPENAI_API_KEY: str
    
    # Stripe API設定
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # データベース設定
    DATABASE_URL: str
    
    # Firebase設定（必須項目として定義）
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(..., env="GOOGLE_APPLICATION_CREDENTIALS")

    model_config: ConfigDict = {
         "env_file": ".env",           # .env ファイルから環境変数を読み込む
         "extra": "allow",             # 未定義の環境変数も許容する
         "case_sensitive": True,       # 大文字小文字を区別する
    }

settings = Settings()
