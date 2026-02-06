# api_server.py
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastmcp import Client
import uvicorn
import json

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# 1. 환경 설정
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_SERVER_URL = "http://localhost:8002/sse"  # Fashion Server 주소

# 2. FastAPI 앱 생성
app = FastAPI(title="AI Stylist API")

# CORS 설정 (React 연동 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 시스템 프롬프트
SYSTEM_INSTRUCTION = """
당신은 패션 어시스턴트입니다. 사용자의 질문에 답하기 위해 반드시 제공된 도구(tools)를 사용해야 합니다.
절대 추측하지 말고, 반드시 도구를 호출해서 정보를 얻은 후 답변하세요.
"""

# 3. 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    query: str  # 예: "ideabong 오늘 뭐 입어?"

# 4. OpenAI 클라이언트 생성 (전역으로 한 번만)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# MCP 도구를 OpenAI 함수 형식으로 변환
def convert_mcp_tools_to_openai(mcp_tools):
    """MCP 도구 목록을 OpenAI function calling 형식으로 변환"""
    openai_tools = []
    for tool in mcp_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') and tool.inputSchema else {"type": "object", "properties": {}}
            }
        }
        openai_tools.append(openai_tool)
    return openai_tools

# 5. 서버 시작 시 도구 목록 출력
@app.on_event("startup")
async def startup_event():
    logger.info("📡 MCP 서버에 연결하여 도구 목록 확인 중...")
    try:
        mcp_client = Client(MCP_SERVER_URL)
        async with mcp_client:
            tools_list = await mcp_client.list_tools()
            logger.info(f"📦 사용 가능한 도구 ({len(tools_list)}개):")
            for tool in tools_list:
                logger.info(f"   📌 {tool.name}")
                logger.info(f"      설명: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    params = tool.inputSchema.get('properties', {})
                    if params:
                        logger.info(f"      파라미터: {list(params.keys())}")
    except Exception as e:
        logger.warning(f"⚠️ MCP 서버 연결 실패: {e}")

# 6. API 엔드포인트 생성
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    React에서 질문을 받아 OpenAI Agent를 실행하고 결과를 반환합니다.
    """
    logger.info(f"📨 요청 받음: {request.query}")

    try:
        # (1) MCP 클라이언트 연결
        mcp_client = Client(MCP_SERVER_URL)

        # (2) 에이전트 실행 로직
        async with mcp_client:
            logger.info("✅ MCP 서버 연결 성공")

            # MCP 도구 목록 가져오기
            mcp_tools = await mcp_client.list_tools()
            openai_tools = convert_mcp_tools_to_openai(mcp_tools)
            logger.info(f"🔧 변환된 OpenAI 도구: {[t['function']['name'] for t in openai_tools]}")

            # 메시지 초기화
            messages = [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": request.query}
            ]

            # OpenAI API 호출 (도구 사용 가능)
            response = await openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=openai_tools if openai_tools else None,
                tool_choice="auto" if openai_tools else None,
                temperature=0
            )

            assistant_message = response.choices[0].message

            # 도구 호출이 필요한 경우 처리
            while assistant_message.tool_calls:
                logger.info(f"🔧 도구 호출 감지: {len(assistant_message.tool_calls)}개")
                
                # 어시스턴트 메시지 추가
                messages.append(assistant_message)

                # 각 도구 호출 처리
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"   📌 도구 실행: {function_name}({function_args})")
                    
                    # MCP를 통해 도구 실행
                    result = await mcp_client.call_tool(function_name, function_args)
                    tool_result = str(result.content[0].text) if result.content else "결과 없음"
                    
                    logger.info(f"   ✅ 도구 결과: {tool_result}")
                    
                    # 도구 결과를 메시지에 추가
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })

                # 도구 결과를 바탕으로 다시 응답 생성
                response = await openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    tools=openai_tools if openai_tools else None,
                    tool_choice="auto" if openai_tools else None,
                    temperature=0
                )
                assistant_message = response.choices[0].message

            final_response = assistant_message.content
            logger.info(f"✅ 응답 생성 완료")
            logger.info(f"📊 응답 텍스트 길이: {len(final_response) if final_response else 0}")

            # (3) 결과 반환
            return {"response": final_response}

    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """서버 상태 확인용"""
    return {"status": "ok", "mcp_server": MCP_SERVER_URL}

if __name__ == "__main__":
    logger.info("🚀 AI Stylist API 서버 시작 (포트: 8004)")
    uvicorn.run(app, host="0.0.0.0", port=8004)