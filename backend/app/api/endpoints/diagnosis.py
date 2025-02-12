from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/free")
async def create_free_diagnosis(request: DiagnosisRequest):
    try:
        # 既存のコード
        result = await process_diagnosis(request)
        return result
    except Exception as e:
        logger.error(f"Error in free diagnosis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    ) 