from fastapi import APIRouter, HTTPException
from ..schemas.diagnosis import (
    FreeDiagnosisRequest,
    FreeDiagnosisResponse,
    DetailedDiagnosisRequest,
    DetailedDiagnosisResponse
)
from ..services.openai_service import openai_service
from ..errors import DiagnosisError, OpenAIError
from ..services.pdf_service import pdf_service
from fastapi.responses import Response
from ..services.diagnosis_store import diagnosis_store
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/free", response_model=FreeDiagnosisResponse)
async def create_free_diagnosis(request: FreeDiagnosisRequest):
    """
    無料診断を実行し、結果を返却する
    """
    try:
        logger.debug(f"Received free diagnosis request for {request.name}")
        
        # OpenAI APIを使用して診断結果を生成
        try:
            result = await openai_service.generate_free_diagnosis(
                name=request.name,
                birth_date=str(request.birth_date)
            )
            logger.debug("Successfully generated diagnosis result from OpenAI")
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            raise
        
        # 診断結果を保存
        try:
            diagnosis_token = await diagnosis_store.create_diagnosis(
                name=request.name,
                birth_date=str(request.birth_date),
                result=result,
                is_detailed=False
            )
            logger.debug(f"Successfully saved diagnosis with token: {diagnosis_token}")
        except DiagnosisError as e:
            logger.error(f"Failed to save diagnosis: {str(e)}", exc_info=True)
            raise
        
        return FreeDiagnosisResponse(
            diagnosis_token=diagnosis_token,
            result=result
        )
    except OpenAIError as e:
        logger.error(f"OpenAI error in create_free_diagnosis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except DiagnosisError as e:
        logger.error(f"Diagnosis error in create_free_diagnosis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_free_diagnosis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

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
        
        # 診断結果を保存
        diagnosis_token = await diagnosis_store.create_diagnosis(
            name=request.name,
            birth_date=str(request.birth_date),
            result=full_result,
            categories=request.categories,
            free_text=request.free_text,
            is_detailed=True
        )
        
        # モザイク処理(仮実装:実際にはより複雑な処理が必要)
        partial_result = full_result[:200] + "...\n\n※ 続きは課金後にご覧いただけます"
        
        return DetailedDiagnosisResponse(
            diagnosis_token=diagnosis_token,
            partial_result=partial_result,
            is_locked=True
        )
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{token}/pdf")
async def download_diagnosis_pdf(token: str):
    """
    診断結果のPDFをダウンロードする
    """
    try:
        diagnosis = await diagnosis_store.get_diagnosis(token)
        if not diagnosis.get('is_unlocked'):
            raise HTTPException(status_code=403, detail="診断結果がロックされています")

        pdf_content = pdf_service.generate_pdf(
            name=diagnosis['name'],
            birth_date=diagnosis['birth_date'],
            result=diagnosis['result']
        )
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="diagnosis-{token}.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
