from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
import random
import string
from langchain_core.messages import SystemMessage, HumanMessage
import pickle
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.tools import langTools
from src.tools import prompt
from util.apiKey import getApiKey



class QA_Chain:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=getApiKey("OPENAI_API_KEY"), streaming=True)
        tools = langTools.LangTools()
        allTools = tools.getAllTools()
        self.memory = MemorySaver()
        

        self.graph = create_react_agent(
            llm,
            tools=allTools,
            checkpointer=self.memory
        )


    def generate_key(self,length=50):
        if length > 50:
            raise ValueError("키 길이는 50자를 넘을 수 없습니다.")
        characters = string.ascii_letters + string.digits  # 영문자 대소문자 + 숫자
        return ''.join(random.choices(characters, k=length))
    

    def __load_chatHistory(self, chatId):
        with open(f"{getApiKey('CHAT_SAVE_URL')}/{chatId}.pkl", "rb")as f:
            result = pickle.load(f)

        return result
    
    def getChatHistory(self, chatId):
        try:
            chatHistory = self.__load_chatHistory(chatId)
            state = chatHistory.get("graph_state").values
            contents = [{"type": msg.type, "msg":msg.content} for msg in state["messages"] if msg.content != "" if msg.type == "human" or msg.type == "ai"]
            return contents
        except Exception as e:
            return f"error to get chatHistory: {e}" #기회되면 여기에 error logging 넣기

    def question(self, query, chatId):
        messages = []
        if not os.path.exists(f"{getApiKey('CHAT_SAVE_URL')}/{chatId}.pkl"): #첫 대화 시
            self.config = {"configurable": {"thread_id": chatId}}
            messages = [
                SystemMessage(content=prompt.systemPrompt()),
                HumanMessage(content=query)
            ]
            print(f"이전 state:{self.graph.get_state(self.config)}")
        else: # 기존 대화 시
            try:
                chatHistory = self.__load_chatHistory(chatId)
                self.config = chatHistory.get("memory_config")
                self.graph.update_state(chatHistory.get("memory_config"), chatHistory.get("graph_state").values)
                messages = [
                    HumanMessage(content=query)
                ]
                # print(f"업데이트 state:{self.graph.get_state(self.config)}") #debug
            except Exception as e:
                print(f"error to get chatHistory: {e}") #기회되면 여기에 error logging 넣기


        for message, metadata in self.graph.stream({"messages": messages}, config=self.config, stream_mode="messages"):
            if metadata["langgraph_node"] == "agent":
                # print(message.content, flush=True)
                yield message.content
        else:
            # 시간나면 예전 내역들 요약하는 것도 구현하기
            # https://velog.io/@euisuk-chung/LangChain-Academy-Introduction-to-LangGraph-Module-2
            with open(f"{getApiKey('CHAT_SAVE_URL')}/{chatId}.pkl", "wb") as f:
                pickle.dump({
                    "memory_config": self.config,
                    "graph_state": self.graph.get_state(self.config)
                }, f)

            return

