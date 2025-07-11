from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import StreamingResponse
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.dependency.modules import get_langAgent
from src.chains.qa_chain import QA_Chain

lcRouter = APIRouter() 

class requestSuggest(BaseModel):
    query: str
    chat_id: str


@lcRouter.post("/suggest")
async def suggest(sug: requestSuggest, lang_agent=Depends(get_langAgent)):
    # lang_agent = await get_langAgent(req) #여길 await로 안하면 coroutine타입으로 받게됨

    async def event_stream():
        # lang_agent.question 이 async generator 라면 이렇게:
        for msg in lang_agent.question(sug.query, sug.chat_id if sug.chat_id else None):
            yield msg
        # else:
        #     yield '[DONE]'

        return

        # 만약 단순 async 함수가 list[str] 반환한다면 이렇게:
        # for msg in await lang_agent.question(sug.query):
        #     yield f"data: {msg}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@lcRouter.get("/createchat")
async def getChat(lang_agent=Depends(get_langAgent)):
    try:
        chat_id = lang_agent.generate_key()
        return {"status": "success", "code":200, "chat_id": chat_id}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "GENERATE_CHATKEY_ERROR",
                "message": "채팅 key를 생성하는데 문제가 발생했습니다."
            }
        )

@lcRouter.get("/get_chat/{chat_id}")
async def getChat(chat_id: str, lang_agent=Depends(get_langAgent)):
    try:
        result = lang_agent.getChatHistory(chat_id)
        return {"status": "success", "code":200, "data": result}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "GET_CHATHISTORY_ERROR",
                "message": "채팅내역을 가져오는데 실패했습니다"
            }
        )