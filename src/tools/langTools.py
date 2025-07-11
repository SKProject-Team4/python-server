from langchain_core.tools import tool 
import xml.etree.ElementTree as ET
from typing import List
import json
from pydantic import BaseModel, Field
import requests
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from util.apiKey import getApiKey

class Travel_Input(BaseModel):
    region: str = Field(description="질문 내용에서 지역명을 추출하여 입력하세요.")
    contentType: str = Field(description="질문 내용에서 여행지 카테고리를 추출하여 입력하세요. 없으면 '관광지'로 입력하세요.")

class LangTools:
    def getAllTools(self):
        return [self.travel_api]
    
    def getAllToolNames(self):
        return ["travel_search_tool"]
    

    # @tool
    # def search_web(query) -> List[str]:
    #     """데이터베이스에 존재하지 않는 정보 또는 최신 정보를 인터넷에서 검색합니다."""

    #     tavily_search = TavilySearchResults(max_results=3)
    #     docs = tavily_search.invoke(query)

    #     formatted_docs = "\n\n---\n\n".join(
    #         [
    #             f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
    #             for doc in docs
    #         ]
    #     )

    #     if len(docs) > 0:
    #         return formatted_docs
        
    #     return "관련 정보를 찾을 수 없습니다."
    
    @tool("travel_search_tool", args_schema=Travel_Input)
    def travel_api(region, contentType) -> List[str]:
        """여행지 혹은 식당 등 추천을 요청하면 이 도구를 사용하여, 사용자에게 추천 여행지 리스트를 제공합니다. **첫 대화일 경우 무조건 이 도구를 사용합니다**"""

        contentTypeDict = {
            "관광지": "12",
            "문화시설": "14",
            "축제공연행사":"15", 
            "여행코스":"25", 
            "레포츠":"28", 
            "숙박":"32", 
            "쇼핑":"38", 
            "음식점":"39"
        }

        sigunguCodeDict = {
            "서울": "1",
            "인천": "2",
            "대전":  "3",
            "대구": "4" ,
            "광주": "5" ,
            "부산": "6" ,
            "울산" : "7",
            "세종시": "8" ,
            "경기도": "31" ,
            "강원도": "32" 
        }

        #동 입력하는것도 필요함

        TRAVEL_URL = f"http://apis.data.go.kr/B551011/KorService2/areaBasedList2?MobileOS=WEB&MobileApp=TEST&areaCode={sigunguCodeDict.get(region)}&contentTypeId={contentTypeDict.get(contentType)}&serviceKey={getApiKey('OPENAPI_API_KEY')}"
        resultListJsonStr = ""
        try:
            response = requests.get(url=TRAVEL_URL)
            response.raise_for_status()  # 응답 코드가 200이 아니면 예외 발생


            # XML 응답 파싱
            root = ET.fromstring(response.text)

            # 모든 <item> 태그 찾기
            items = root.findall(".//item")

            # print(f"총 {len(items)}개의 항목을 찾았습니다.\n")

            resultListJsonStr = json.dumps([
                {
                    "title": item.findtext("title", default="제목 없음"),
                    "address": item.findtext("addr1", default="주소 없음")
                }
                for item in items
            ], ensure_ascii=False, indent=2)  # ensure_ascii=False는 한글 깨짐 방지용

            # print(resultListJsonStr)

            # for item in items:
            #     title = item.findtext("title", default="제목 없음")
            #     address = item.findtext("addr1", default="주소 없음")
            #     image_url = item.findtext("firstimage", default="이미지 없음")
            #     map_x = item.findtext("mapx", default="좌표 없음")
            #     map_y = item.findtext("mapy", default="좌표 없음")


        except requests.exceptions.HTTPError as http_err:
            return f"HTTP 오류 발생: {http_err}"
        except requests.exceptions.RequestException as err:
            return f"요청 오류 발생: {err}"
        except ValueError:
            return "응답을 JSON으로 변환할 수 없습니다."
        else:
            return resultListJsonStr


