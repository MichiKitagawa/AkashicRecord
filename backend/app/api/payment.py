from fastapi import APIRouter, Header, Request
from ..services.stripe_service import stripe_service
from ..schemas.payment import CreateCheckoutSessionRequest, CreateCheckoutSessionResponse

router = APIRouter()

@router.post("/create-checkout-session", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """
    Stripe Checkoutセッションを作成する
    """
    checkout_url = await stripe_service.create_checkout_session(request.diagnosis_token)
    return CreateCheckoutSessionResponse(checkout_url=checkout_url)

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Stripeからのwebhookを処理する
    """
    payload = await request.body()
    await stripe_service.handle_webhook(payload, stripe_signature)
    return {"status": "success"} 