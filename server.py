# server.py
import logging
from fastmcp import FastMCP

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# 1. MCP 서버 생성 (이름: Fashion Server)
mcp = FastMCP("Fashion Server")

# 2. 데이터 (DB 대용)
members_db = {
    "ideabong": {"name": "이상봉", "location": "Seoul", "style": "스트릿 패션", "gender": "남성"},
    "sunny": {"name": "박써니", "location": "Busan", "style": "러블리 캐주얼", "gender": "여성"}
}

ootd_log = {
    "monday": "검정 슬랙스에 흰 셔츠",
    "tuesday": "청바지에 후드티",
    "wednesday": "트레이닝복 세트"
}

# 3. 도구(Tool) 등록하기 🛠️
# AI는 이 '함수 이름'과 '설명(Docstring)'을 읽고 사용 여부를 결정합니다.

@mcp.tool()
def get_member_profile(name: str) -> str:
    """
    팀원의 이름(name)을 입력하면 성별, 선호 스타일, 거주지 정보를 반환합니다.
    등록된 팀원: ideabong, sunny
    """
    logger.info(f"🔧 [get_member_profile] 호출됨 | 입력: name='{name}'")
    member = members_db.get(name)
    if not member:
        result = "존재하지 않는 팀원입니다."
        logger.warning(f"   ⚠️ 결과: {result}")
        return result
    result = str(member)
    logger.info(f"   ✅ 결과: {result}")
    return result

@mcp.tool()
def get_ootd_history(day: str) -> str:
    """
    특정 요일(day)에 입었던 옷차림(OOTD) 기록을 반환합니다.
    입력 예시: monday, tuesday, wednesday
    """
    logger.info(f"🔧 [get_ootd_history] 호출됨 | 입력: day='{day}'")
    result = ootd_log.get(day, "기록 없음")
    logger.info(f"   ✅ 결과: {result}")
    return result

@mcp.tool()
def get_current_weather(location: str) -> str:
    """
    도시 이름(location)을 입력하면 현재 날씨를 반환합니다.
    지원 도시: Seoul, Busan
    """
    logger.info(f"🔧 [get_current_weather] 호출됨 | 입력: location='{location}'")
    # 실습을 위해 날씨 API 대신 고정값을 반환합니다.
    weather_data = {
        "Seoul": "15도, 맑음, 바람 약간",
        "Busan": "20도, 화창함"
    }
    result = weather_data.get(location, "알 수 없는 지역")
    logger.info(f"   ✅ 결과: {result}")
    return result

# 4. 서버 실행
if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("🚀 Fashion Server 시작 중...")
    logger.info(f"📦 등록된 도구: get_member_profile, get_ootd_history, get_current_weather")
    logger.info(f"👥 등록된 멤버: {list(members_db.keys())}")
    logger.info("=" * 50)
    mcp.run(transport="sse", port=8002)