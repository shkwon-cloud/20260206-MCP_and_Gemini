# agent.py
import asyncio
import os
import logging
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastmcp import Client

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# 1. 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. 로컬에 떠 있는 MCP 서버(Fashion Server)에 연결
MCP_SERVER_URL = "http://localhost:8002/sse"
mcp_client = Client(MCP_SERVER_URL)

# 3. OpenAI 클라이언트 생성
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# 시스템 프롬프트
SYSTEM_INSTRUCTION = """
당신은 패션 어시스턴트입니다. 사용자의 질문에 답하기 위해 반드시 제공된 도구(tools)를 사용해야 합니다.
절대 추측하지 말고, 반드시 도구를 호출해서 정보를 얻은 후 답변하세요.
"""

async def main():
    logger.info("=" * 60)
    logger.info("🤖 OpenAI Agent 시작")
    logger.info(f"🔗 MCP 서버 URL: {MCP_SERVER_URL}")
    logger.info("=" * 60)

    # MCP 클라이언트 세션 시작
    logger.info("📡 MCP 서버에 연결 중...")
    async with mcp_client:
        logger.info("✅ MCP 서버 연결 성공!")

        # 사용 가능한 도구 목록 확인
        tools_list = await mcp_client.list_tools()
        logger.info(f"📦 사용 가능한 도구 ({len(tools_list)}개):")
        
        # OpenAI 형식으로 도구 변환
        openai_tools = []
        for tool in tools_list:
            logger.info(f"   - {tool.name}: {tool.description[:50]}...")
            # MCP 도구의 inputSchema를 OpenAI의 parameters로 맵핑
            # inputSchema가 직접 도구 객체에 없을 경우를 대비해 딕셔너리 변환 시도
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": getattr(tool, 'inputSchema', {}),
                }
            })

        # 질문 정의
        user_query = "ideabong에게 오늘 날씨에 맞춰서 옷을 추천해줘. 지난주 화요일에 입은 거랑 안 겹치게 해줘."

        logger.info("-" * 60)
        logger.info(f"🙋 사용자 질문: {user_query}")
        logger.info("-" * 60)

        # 메시지 히스토리 초기화
        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_query}
        ]

        logger.info("🧠 OpenAI API 호출 중... (도구 활용)")

        # 1. 초기 호출
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=openai_tools,
            temperature=0,
        )

        # 2. 도구 호출 루프
        while response.choices[0].message.tool_calls:
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            tool_calls = assistant_message.tool_calls
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"🛠️ MCP 도구 호출: {tool_name}({tool_args})")
                
                try:
                    # mcp_client.call_tool을 사용하여 실제 도구 실행
                    call_result = await mcp_client.call_tool(tool_name, tool_args)
                    
                    # 결과에서 텍스트 추출
                    tool_output = ""
                    if hasattr(call_result, 'content'):
                        # typical MCP content is a list of TextContent/ImageContent
                        tool_output = "\n".join([
                            c.text for c in call_result.content 
                            if hasattr(c, 'text')
                        ])
                    else:
                        tool_output = str(call_result)
                        
                except Exception as e:
                    tool_output = f"오류 발생: {str(e)}"
                    logger.error(f"   ❌ 도구 호출 실패: {tool_output}")

                logger.info(f"   ✅ 결과: {tool_output[:100]}...")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_output,
                })

            # 도구 결과를 포함하여 다시 호출
            response = await openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=openai_tools,
                temperature=0,
            )

        # 최종 응답 추출
        final_response = response.choices[0].message.content

        # 응답 메타데이터 출력
        logger.info("-" * 60)
        logger.info("📊 응답 메타데이터:")
        logger.info(f"   - model: {response.model}")
        if hasattr(response, 'usage'):
            logger.info(f"   - 입력 토큰: {response.usage.prompt_tokens}")
            logger.info(f"   - 출력 토큰: {response.usage.completion_tokens}")

        logger.info("-" * 60)
        logger.info("🤖 OpenAI 응답:")
        logger.info("-" * 60)
        print(f"\n{final_response}\n")
        logger.info("=" * 60)
        logger.info("✅ Agent 작업 완료!")
        logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())