# agent.py
import asyncio
import os
import logging
from dotenv import load_dotenv
from google import genai
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. 로컬에 떠 있는 MCP 서버(Fashion Server)에 연결
MCP_SERVER_URL = "http://localhost:8002/sse"
mcp_client = Client(MCP_SERVER_URL)

# 3. Gemini 클라이언트 생성
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 시스템 프롬프트
SYSTEM_INSTRUCTION = """
당신은 패션 어시스턴트입니다. 사용자의 질문에 답하기 위해 반드시 제공된 도구(tools)를 사용해야 합니다.
절대 추측하지 말고, 반드시 도구를 호출해서 정보를 얻은 후 답변하세요.
"""

async def main():
    logger.info("=" * 60)
    logger.info("🤖 Gemini Agent 시작")
    logger.info(f"🔗 MCP 서버 URL: {MCP_SERVER_URL}")
    logger.info("=" * 60)

    # MCP 클라이언트 세션 시작
    logger.info("📡 MCP 서버에 연결 중...")
    async with mcp_client:
        logger.info("✅ MCP 서버 연결 성공!")

        # 사용 가능한 도구 목록 확인
        tools_list = await mcp_client.list_tools()
        logger.info(f"📦 사용 가능한 도구 ({len(tools_list)}개):")
        for tool in tools_list:
            logger.info(f"   - {tool.name}: {tool.description[:50]}...")

        # 질문 정의
        user_query = "ideabong에게 오늘 날씨에 맞춰서 옷을 추천해줘. 지난주 화요일에 입은 거랑 안 겹치게 해줘."

        logger.info("-" * 60)
        logger.info(f"🙋 사용자 질문: {user_query}")
        logger.info("-" * 60)

        # FastMCP Client의 세션 객체 가져오기
        session = mcp_client.session
        logger.info(f"🔧 MCP 세션 타입: {type(session).__name__}")

        # Gemini API 호출
        logger.info("🧠 Gemini API 호출 중... (도구 자동 호출 활성화)")

        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_query,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0,
                tools=[session],
            ),
        )

        # 응답 메타데이터 출력
        logger.info("-" * 60)
        logger.info("📊 응답 메타데이터:")
        if response.candidates:
            candidate = response.candidates[0]
            logger.info(f"   - finish_reason: {candidate.finish_reason}")
            if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                for rating in candidate.safety_ratings[:2]:  # 처음 2개만
                    logger.info(f"   - safety: {rating.category} = {rating.probability}")

        # 사용량 정보 (있을 경우)
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = response.usage_metadata
            logger.info(f"   - 입력 토큰: {getattr(usage, 'prompt_token_count', 'N/A')}")
            logger.info(f"   - 출력 토큰: {getattr(usage, 'candidates_token_count', 'N/A')}")

        logger.info("-" * 60)
        logger.info("🤖 Gemini 응답:")
        logger.info("-" * 60)
        print(f"\n{response.text}\n")
        logger.info("=" * 60)
        logger.info("✅ Agent 작업 완료!")
        logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())