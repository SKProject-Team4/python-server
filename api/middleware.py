from starlette.middleware.base import BaseHTTPMiddleware
import logging 
from multiprocessing import Queue
from pythonjsonlogger import jsonlogger
from logging_loki import LokiQueueHandler
import time
import sys, os 
from fastapi import HTTPException
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.dependency.modules import get_redis 
from util.jwt import checkJWTToken
from util.apiKey import getApiKey

allow_origin_list = [
    "" #추후 추가할것
]

loki_handler = LokiQueueHandler(
    Queue(-1), #무한개의 큐 준비
    url=getApiKey("LOKI_ENDPOINT"),
    tags={"application": "fastapi", "logtype": "request"},
    version="1"
)

#getLogger의 이름이 uvicorn.access이면 logger를 사용하지 않더라도 자동으로 logging이 됨(deprecated)
# uvicorn_access_logger = logging.getLogger("uvicorn.access")
# uvicorn_access_logger.addHandler(loki_handler)

formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s %(method)s %(path)s %(ip)s %(user_agent)s %(response_time)s %(user_id)s %(username)s %(role)s'
)
loki_handler.setFormatter(formatter)

user_logger = logging.getLogger("fastapi.request.logger")
user_logger.setLevel(logging.INFO) #INFO 레벨 이상 모두 로깅
user_logger.addHandler(loki_handler)

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        redis_client = await get_redis(request)

        #ip주소
        client_ip = request.client.host if request.client else "unknown"


        token = request.headers["Authorization"].split(' ')[1] # 'Bearer TOKEN'에서 TOKEN 부분만 추출
        if await redis_client.get(token) is None: #redis에 값이 없을 경우 인증오류를 반환함
            raise HTTPException(status_code=401, detail={
                "code": "INVALID_REQUEST",
                "message": "요청 형식이 올바르지 않습니다."
            })
        
        tokenCheckResult = checkJWTToken(token) #tokenCheckResult에서 디코딩된 내용으로 user_info내용 수정할것

        print(token)
        print(tokenCheckResult)
        # 기본 사용자 정보 (기본값: 익명)
        user_info = {
            "user_id": tokenCheckResult.get("userId",None),
            "username": tokenCheckResult.get("username","anonymous"),
            "role": tokenCheckResult.get("role","guest")
        }

        if tokenCheckResult.get("success") == False:
            raise HTTPException(status_code=401, detail={
                "code": "INVALID_TOKEN",
                "message": tokenCheckResult.get("error")
            })
        
        response = await call_next(request)

        # 응답 시간 계산
        duration = round((time.time() - start_time) * 1000, 2)  # ms

        # 로그 전송
        user_logger.info(
            "Request log",
            extra={
                "method": request.method,
                "token": token,
                "path": request.url.path,
                "ip": client_ip,
                "response_time": duration,
                **user_info, # ** = 딕셔너리형태로 전달
            }
        )

        response.headers["Access-Control-Allow-Origin"] = "*"

        return response
