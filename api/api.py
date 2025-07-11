from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from middleware import CustomMiddleware
from router.langchainRouter import lcRouter
from dependency import modules
from util.responseModel import ErrorResponse, ErrorDetail


app = FastAPI(lifespan=modules.lifespan) 
#lifespan은 @app.on_event("startup") 대신에 쓰는 방식 최신 FastAPI에 도입됨.


app.add_middleware(CustomMiddleware)

app.include_router(lcRouter, prefix="/chat")

#에러 예외사항 응답처리기
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.status_code,
                error=ErrorDetail(
                    code=detail.get("code", "HTTP_EXCEPTION"),
                    message=detail.get("message", "에러가 발생했습니다.")
                )
            ).model_dump()
    )

@app.get("/health-check", status_code=200)
def check():
    return {"success": True}