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

        client_ip = request.client.host if request.client else "unknown"
        token = None
        user_info = {
            "user_id": None,
            "username": "anonymous",
            "role": "guest"
        }

        auth_header = request.headers.get("Authorization")
        if auth_header and isinstance(auth_header, str) and auth_header.startswith("Bearer "):
            parts = auth_header.split(" ", 1)
            if len(parts) == 2:
                token = parts[1]

            tokenCheckResult = checkJWTToken(token)

            print(token)
            print(tokenCheckResult)

            if tokenCheckResult.get("success") == False:
                raise HTTPException(status_code=401, detail={
                    "code": "INVALID_TOKEN",
                    "message": tokenCheckResult.get("error")
                })

            if await redis_client.get(token) is None:
                raise HTTPException(status_code=401, detail={
                    "code": "INVALID_REQUEST",
                    "message": "요청 형식이 올바르지 않습니다."
                })

            user_info.update({
                "user_id": tokenCheckResult.get("userId"),
                "username": tokenCheckResult.get("username", "anonymous"),
                "role": tokenCheckResult.get("role", "guest")
            })

        response = await call_next(request)

        duration = round((time.time() - start_time) * 1000, 2)

        user_logger.info(
            "Request log",
            extra={
                "method": request.method,
                "token": token,
                "path": request.url.path,
                "ip": client_ip,
                "response_time": duration,
                **user_info
            }
        )

        response.headers["Access-Control-Allow-Origin"] = "*"

        return response

