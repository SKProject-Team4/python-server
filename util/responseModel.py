from pydantic import BaseModel 

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    status: str = "error"
    code: int
    error: ErrorDetail

