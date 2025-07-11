import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET
import os, sys
import requests
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.apiKey import getApiKey
from src.tools import langTools
from src.chains import qa_chain

# chain_module = qa_chian.QA_Chain()

# class LangchainTest(unittest.TestCase):
#     def checkQuestionRouter(self):
#         result = chain_module.question_tool_router.invoke({"question": "근로계약 체결할 때 개인정보 취급 상의 유의사항은 무엇인가요?"})
#         self.assertEqual(type(result), str)
        

def main():
    import pickle
    test = langTools.LangTools()
    # print(test.travel_api.args)
    # print(test.travel_api.invoke({
    #     "region": "서울",
    #     "contentType": "음식점"
    # }))
    chain_module = qa_chain.QA_Chain()
    print(chain_module.getChatHistory("PMhzIbmMLW7dAYsBv308yBI5S9CTs7PaYJERc1waNsWokkstII"))
    # for msg in chain_module.question("아까 내가 뭐랬지?", "PMhzIbmMLW7dAYsBv308yBI5S9CTs7PaYJERc1waNsWokkstII"):
    #     print(msg)






if __name__ == "__main__":
    # unittest.main()
    main()