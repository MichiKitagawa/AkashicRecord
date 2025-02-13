from fastapi import APIRouter, Header, Request
from ..services.stripe_service import stripe_service
from ..schemas.payment import CreateCheckoutSessionRequest, CreateCheckoutSessionResponse
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/create-checkout-session", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """
    Stripe Checkoutセッションを作成する
    """
    logger.debug(f"チェックアウトセッション作成リクエスト: {request.diagnosis_token}")
    checkout_url = await stripe_service.create_checkout_session(request.diagnosis_token)
    logger.debug(f"チェックアウトURL生成完了: {checkout_url}")
    return CreateCheckoutSessionResponse(checkout_url=checkout_url)

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Stripeからのwebhookを処理する
    """
    try:
        logger.debug("Webhook受信開始")
        logger.debug(f"Stripe-Signature: {stripe_signature}")
        
        payload = await request.body()
        logger.debug(f"受信したペイロード: {payload.decode()}")
        
        await stripe_service.handle_webhook(payload, stripe_signature)
        logger.debug("Webhook処理完了")
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook処理エラー: {str(e)}", exc_info=True)
        raise 