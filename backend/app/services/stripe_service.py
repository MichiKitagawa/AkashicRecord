import stripe
from ..core.config import settings
from ..errors import PaymentError
from ..services.diagnosis_store import diagnosis_store
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class StripeService:
    def __init__(self):
        logger.debug(f"Stripe APIキーを設定: {settings.STRIPE_SECRET_KEY[:8]}...")
        stripe.api_key = settings.STRIPE_SECRET_KEY

    async def create_checkout_session(self, diagnosis_token: str) -> str:
        """
        Stripeの決済セッションを作成する
        """
        try:
            logger.debug(f"チェックアウトセッション作成開始: {diagnosis_token}")
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
            logger.debug(f"チェックアウトセッション作成完了: {session.id}")
            return session.url
        except stripe.error.StripeError as e:
            logger.error(f"Stripeエラー: {str(e)}")
            raise PaymentError(str(e))
        except Exception as e:
            logger.error(f"予期せぬエラー: {str(e)}")
            raise PaymentError(str(e))

    async def handle_webhook(self, payload: str, signature: str) -> None:
        """
        Stripeからのwebhookを処理する
        """
        try:
            logger.debug("Webhookイベントの検証開始")
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )
            logger.debug(f"Webhookイベントタイプ: {event.type}")

            if event.type == 'checkout.session.completed':
                session = event.data.object
                diagnosis_token = session.metadata.get('diagnosis_token')
                logger.debug(f"決済完了: セッションID {session.id}, 診断トークン {diagnosis_token}")
                
                if diagnosis_token:
                    await diagnosis_store.unlock_diagnosis(diagnosis_token)
                    logger.debug(f"診断結果のロック解除完了: {diagnosis_token}")

        except stripe.error.SignatureVerificationError as e:
            logger.error(f"署名検証エラー: {str(e)}")
            raise PaymentError("Invalid signature")
        except Exception as e:
            logger.error(f"Webhook処理エラー: {str(e)}")
            raise PaymentError(str(e))

stripe_service = StripeService() 