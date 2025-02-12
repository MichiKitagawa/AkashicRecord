from fastapi import APIRouter, HTTPException
from ..schemas.diagnosis import (
    FreeDiagnosisRequest,
    FreeDiagnosisResponse,
    DetailedDiagnosisRequest,
    DetailedDiagnosisResponse
)
from ..services.openai_service import openai_service

router = APIRouter()

@router.post("/free", response_model=FreeDiagnosisResponse)
async def create_free_diagnosis(request: FreeDiagnosisRequest):
    """
    無料診断を実行し、結果を返却する
    """
    try:
        # OpenAI APIを使用して診断結果を生成
        result = await openai_service.generate_free_diagnosis(
            name=request.name,
            birth_date=str(request.birth_date)
        )
        
        # レスポンスを生成
        return FreeDiagnosisResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detail", response_model=DetailedDiagnosisResponse)
async def create_detailed_diagnosis(request: DetailedDiagnosisRequest):
    """
    有料診断を実行し、モザイク処理された結果を返却する
    """
    try:
        # OpenAI APIを使用して詳細な診断結果を生成
        full_result = await openai_service.generate_detailed_diagnosis(
            name=request.name,
            birth_date=str(request.birth_date),
            categories=request.categories,
            free_text=request.free_text or ""
        )
        
        # モザイク処理(仮実装:実際にはより複雑な処理が必要)
        partial_result = full_result[:200] + "...\n\n※ 続きは課金後にご覧いただけます"
        
        # レスポンスを生成
        return DetailedDiagnosisResponse(partial_result=partial_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
