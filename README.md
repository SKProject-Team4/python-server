## Planmate  
> 여행이 쉬워진다, AI와 함께라면.  

### 기술 스택  
    - Server  
        - Python
        - FastAPI
        - Langchain
    - Infra
        - Redis
        - Loki
        - Grafana
        - MySQL
        - Adminer
        - K8s

### 디렉토리 구조  
api
    api.py # api 구성코드
    middleware.py # 토큰검사,로깅 미들웨어
router
    langchainRouter.py #langgraph 로직api 라우터
src
    chains
        qa_chains.py #langgraph 핵심로직
    dependency
        modules.py #redis,langgraph 의존성 주입용 객체선언
    tools
        langTools.py #langgraph tool 선언
        prompt.py #prompt 선언
test
    langchainTest.py #langchain 테스트
    redisTest.py #redis 연결테스트
util
    apiKey.py #env 데이터관리
    jwt.py #jwt 관리
    responseModel.py #오류핸들링
.env 
Dockerfile #fastAPI서버 도커파일
requirements.txt #파이썬 모듈들