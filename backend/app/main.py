import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import diagnosis, payment
from .core.config import settings

# ログ設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Akashic AI Divination API",
    description="AI占いサービスのバックエンドAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # フロントエンドのURL
        "https://3b6c-133-155-128-225.ngrok-free.app"  # ngrok URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(diagnosis.router, prefix="/api/diagnosis")
app.include_router(payment.router, prefix="/api/payment")

@app.get("/")
async def root():
    return {"message": "Akashic AI Divination API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
