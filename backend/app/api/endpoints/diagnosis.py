from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
from app.services.openai_service import generate_diagnosis  # OpenAIサービスをインポート
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.diagnosis import create_diagnosis

# ロガーの設定を追加
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# リクエストモデルの定義
class DiagnosisRequest(BaseModel):
    name: str
    birth_date: str

# 診断処理の関数
async def process_diagnosis(request: DiagnosisRequest):
    try:
        logger.debug(f"Processing diagnosis for: {request.name}")  # デバッグログ
        # OpenAIを使用して診断結果を生成
        result = await generate_diagnosis(request.name, request.birth_date)
        logger.debug(f"Diagnosis result: {result}")  # デバッグログ
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in process_diagnosis: {str(e)}", exc_info=True)  # スタックトレースを含むエラーログ
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/free")
async def create_free_diagnosis(
    request: DiagnosisRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.debug(f"Received request: {request}")  # デバッグログ
        result = await generate_diagnosis(request.name, request.birth_date)
        # データベースに保存
        diagnosis = await create_diagnosis(
            db=db,
            name=request.name,
            birth_date=request.birth_date,
            result=result
        )
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in free diagnosis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    ) 