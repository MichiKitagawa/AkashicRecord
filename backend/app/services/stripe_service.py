import stripe
from ..config import settings
from ..errors import PaymentError
from ..services.diagnosis_store import diagnosis_store

class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    async def create_checkout_session(self, diagnosis_token: str) -> str:
        """
        Stripeの決済セッションを作成する
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                            'name': 'アカシックAI詳細診断',
                            'description': '詳細な運勢診断結果の閲覧',
                        },
                        'unit_amount': 1000,  # 1,000円
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{settings.FRONTEND_URL}/diagnosis/complete?token={diagnosis_token}",
                cancel_url=f"{settings.FRONTEND_URL}/diagnosis/detail",
                metadata={
                    'diagnosis_token': diagnosis_token
                }
            )
            return session.url
        except stripe.error.StripeError as e:
            raise PaymentError(str(e))

    async def handle_webhook(self, payload: str, signature: str) -> None:
        """
        Stripeからのwebhookを処理する
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )

            if event.type == 'checkout.session.completed':
                session = event.data.object
                diagnosis_token = session.metadata.get('diagnosis_token')
                if diagnosis_token:
                    await diagnosis_store.unlock_diagnosis(diagnosis_token)

        except stripe.error.SignatureVerificationError:
            raise PaymentError("Invalid signature")
        except Exception as e:
            raise PaymentError(str(e))

stripe_service = StripeService() 