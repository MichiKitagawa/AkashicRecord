from fastapi import APIRouter, Header, Request, HTTPException
from ..services.square_service import square_service
from ..schemas.payment import CreateCheckoutSessionRequest, CreateCheckoutSessionResponse
import logging
import json
from ..config import settings

# ロガーの設定
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/create-checkout-session", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """
    Square決済リンクを作成する
    """
    logger.debug(f"決済リンク作成リクエスト: {request.diagnosis_token}")
    checkout_url = await square_service.create_payment_link(request.diagnosis_token)
    logger.debug(f"決済リンク生成完了: {checkout_url}")
    return CreateCheckoutSessionResponse(checkout_url=checkout_url)

@router.post("/webhook")
async def square_webhook(request: Request, signature: str = Header(None, alias="Square-Signature")):
    """
    Squareからのwebhookを処理する
    """
    try:
        logger.debug("Webhook受信開始")
        logger.debug(f"Square-Signature: {signature}")
        
        payload = await request.json()
        logger.debug(f"受信したペイロード: {json.dumps(payload)}")

        # 開発環境の場合でも、webhookの処理を実行
        if settings.ENVIRONMENT == "development":
            logger.debug("開発環境でのWebhook処理を開始")
            await square_service.handle_webhook(payload)
            return {"status": "success"}
            
        # 本番環境の場合は署名検証を実行
        if not square_service.verify_signature(signature, json.dumps(payload)):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        await square_service.handle_webhook(payload)
        logger.debug("Webhook処理完了")
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook処理エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 