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
```
├── api
│   ├── api.py                 # API 구성 코드
│   └── middleware.py          # 토큰 검사 및 로깅 미들웨어
│
├── router
│   └── langchainRouter.py     # LangGraph 로직 API 라우터
│
├── src
│   ├── chains
│   │   └── qa_chains.py       # LangGraph 핵심 로직
│   │
│   ├── dependency
│   │   └── modules.py         # Redis, LangGraph 의존성 주입 객체 선언
│   │
│   └── tools
│       ├── langTools.py       # LangGraph Tool 선언
│       └── prompt.py          # Prompt 선언
│
├── test
│   ├── langchainTest.py       # LangChain 테스트
│   └── redisTest.py           # Redis 연결 테스트
│
├── util
│   ├── apiKey.py              # 환경 변수 관리
│   ├── jwt.py                 # JWT 관리
│   └── responseModel.py       # 오류 핸들링
│
├── .env                       # 환경 변수 설정 파일
├── Dockerfile                 # FastAPI 서버 Dockerfile
└── requirements.txt           # Python 모듈 목록
```
