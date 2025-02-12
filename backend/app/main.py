from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import diagnosis
from .core.config import settings

app = FastAPI(
    title="Akashic AI Divination API",
    description="AI占いサービスのバックエンドAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(diagnosis.router, prefix="/api/diagnosis", tags=["diagnosis"])

@app.get("/")
async def root():
    return {"message": "Akashic AI Divination API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
