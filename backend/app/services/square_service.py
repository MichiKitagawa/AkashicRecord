from square.client import Client
from ..core.config import settings
from ..errors import PaymentError
from ..services.diagnosis_store import diagnosis_store
import logging
import uuid
import hmac
import hashlib
import requests

logger = logging.getLogger(__name__)

class SquareService:
    def __init__(self):
        try:
            self.client = Client(
                access_token=settings.SQUARE_ACCESS_TOKEN,
                environment='sandbox' if settings.ENVIRONMENT == 'development' else 'production'
            )
            self.location_id = settings.SQUARE_LOCATION_ID
            self.webhook_signature_key = settings.SQUARE_WEBHOOK_SIGNATURE_KEY
            logger.debug("Square APIクライアントの初期化が完了しました")
        except Exception as e:
            logger.error(f"Square APIクライアントの初期化に失敗しました: {str(e)}")
            raise PaymentError(f"決済サービスの初期化に失敗しました: {str(e)}")

    def verify_signature(self, signature: str, payload: str) -> bool:
        """
        Webhookの署名を検証する
        """
        try:
            if not signature or not self.webhook_signature_key:
                return False

            calculated_signature = hmac.new(
                self.webhook_signature_key.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(calculated_signature, signature)
        except Exception as e:
            logger.error(f"署名検証エラー: {str(e)}")
            return False

    async def create_payment_link(self, diagnosis_token: str) -> str:
        """
        Square決済リンクを作成する
        """
        try:
            logger.debug(f"決済リンク作成開始: {diagnosis_token}")
            
            redirect_url = f"{settings.FRONTEND_URL}/diagnosis/complete?token={diagnosis_token}"
            logger.debug(f"リダイレクトURL: {redirect_url}")
            
            # 決済リンクを作成
            checkout_request = {
                'idempotency_key': str(uuid.uuid4()),
                'description': 'アカシックAI詳細診断',
                'order': {
                    'location_id': self.location_id,
                    'line_items': [
                        {
                            'name': 'アカシックAI詳細診断',
                            'quantity': '1',
                            'base_price_money': {
                                'amount': 1000,  # 1,000円
                                'currency': 'JPY'
                            }
                        }
                    ],
                    'metadata': {
                        'diagnosis_token': diagnosis_token
                    }
                },
                'payment_note': f'診断ID: {diagnosis_token}',
                'checkout_options': {
                    'redirect_url': redirect_url,
                    'allow_tipping': False,
                    'enable_coupon': False,
                    'enable_loyalty': False
                }
            }
            
            result = self.client.checkout.create_payment_link(checkout_request)
            if result.is_success():
                payment_link = result.body['payment_link']['url']
                logger.debug(f"決済リンク作成完了: {payment_link}")
                return payment_link
            else:
                logger.error(f"決済リンク作成エラー: {result.errors}")
                raise PaymentError(f"決済リンクの作成に失敗しました: {result.errors}")
                
        except Exception as e:
            logger.error(f"決済リンク作成中にエラーが発生しました: {str(e)}")
            raise PaymentError(str(e))

    async def handle_webhook(self, payload: dict) -> None:
        """
        Squareからのwebhookを処理する
        """
        try:
            logger.debug(f"Webhook受信: {payload['type']}")
            
            if payload['type'] == 'payment.completed':
                payment = payload['data']['object']['payment']
                order_id = payment['order_id']
                
                # 注文情報を取得
                order_result = self.client.orders.retrieve_order(order_id)
                if order_result.is_success():
                    order = order_result.body['order']
                    diagnosis_token = order['metadata'].get('diagnosis_token')
                    
                    if diagnosis_token:
                        await diagnosis_store.unlock_diagnosis(diagnosis_token)
                        logger.debug(f"診断結果のロック解除完了: {diagnosis_token}")
                    else:
                        logger.error("診断トークンが見つかりません")
                else:
                    logger.error(f"注文情報の取得に失敗: {order_result.errors}")
                    
        except Exception as e:
            logger.error(f"Webhook処理エラー: {str(e)}")
            raise PaymentError(str(e))

square_service = SquareService() 