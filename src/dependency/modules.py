from redis.asyncio import Redis 
from contextlib import asynccontextmanager # 비동기 리소스를 열고 닫는 과정을 try / finally처럼 구조화할 수 있게 해주는 도구
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import apiKey 
from chains.qa_chain import QA_Chain

#Redis와 Langchain모듈을 의존성주입으로 활용할 코드

@asynccontextmanager #asynccontextmanager는 FastAPI의 lifespan의 인자를 넣기위해 위 어노테이션으로 wrapping해야한다
async def lifespan(app):
    # app.state.redis = Redis.from_url(apiKey.getApiKey("REDIS_URL"), decode_responses=True) #커넥션 풀로 관리됨0
    app.state.redis = Redis.from_url("redis://redis:6379", decode_responses=True) #커넥션 풀로 관리됨0
    # app.state.langagent = QA_Chain() 
    yield # 여기까지 실행되면 FastAPI 앱이 실행됨
    await app.state.redis.close()  # 앱이 종료될 때 실행됨

# Redis 의존성 주입 
async def get_redis(request):
    return request.app.state.redis

# Langchain Agent 의존성 주입 (요청마다 새로 생성)
def get_langAgent():
    # return request.app.state.langagent
    return QA_Chain()