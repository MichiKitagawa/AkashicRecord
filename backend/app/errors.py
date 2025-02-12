from fastapi import HTTPException

class DiagnosisError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class OpenAIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class PaymentError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class PDFGenerationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail) 