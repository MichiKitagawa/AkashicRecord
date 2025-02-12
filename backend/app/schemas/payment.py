from pydantic import BaseModel

class CreateCheckoutSessionRequest(BaseModel):
    diagnosis_token: str

class CreateCheckoutSessionResponse(BaseModel):
    checkout_url: str 