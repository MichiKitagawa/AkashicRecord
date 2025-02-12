from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

class FreeDiagnosisRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="ユーザー名")
    birth_date: date = Field(..., description="生年月日")

class FreeDiagnosisResponse(BaseModel):
    diagnosis_token: str = Field(default_factory=lambda: str(uuid.uuid4()), description="診断ID")
    result: str = Field(..., description="診断結果")

class DetailedDiagnosisRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="ユーザー名")
    birth_date: date = Field(..., description="生年月日")
    categories: List[str] = Field(..., min_items=1, description="占いを希望する分野")
    free_text: Optional[str] = Field(None, max_length=1000, description="具体的な悩みや状況")

class DetailedDiagnosisResponse(BaseModel):
    diagnosis_token: str = Field(default_factory=lambda: str(uuid.uuid4()), description="診断ID")
    partial_result: str = Field(..., description="モザイク処理された診断結果")
    is_locked: bool = Field(default=True, description="課金状態")

class UnlockedDiagnosisResponse(BaseModel):
    diagnosis_token: str = Field(..., description="診断ID")
    full_result: str = Field(..., description="完全な診断結果")
    is_locked: bool = Field(default=False, description="課金状態")
