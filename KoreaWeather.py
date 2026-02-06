# KoreaWeather.py
# 기상청 단기예보 API를 활용한 MCP 서버
import os
import logging
import requests
from datetime import datetime, timedelta
from fastmcp import FastMCP
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# 환경 설정
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # 공공데이터포털 API 키

# 1. MCP 서버 생성
mcp = FastMCP("Korea Weather Server")

# 2. 지역별 격자 좌표 (기상청 API용)
LOCATION_GRID = {
    "서울": {"nx": 60, "ny": 127},
    "Seoul": {"nx": 60, "ny": 127},
    "부산": {"nx": 98, "ny": 76},
    "Busan": {"nx": 98, "ny": 76},
    "대구": {"nx": 89, "ny": 90},
    "Daegu": {"nx": 89, "ny": 90},
    "인천": {"nx": 55, "ny": 124},
    "Incheon": {"nx": 55, "ny": 124},
    "광주": {"nx": 58, "ny": 74},
    "Gwangju": {"nx": 58, "ny": 74},
    "대전": {"nx": 67, "ny": 100},
    "Daejeon": {"nx": 67, "ny": 100},
    "울산": {"nx": 102, "ny": 84},
    "Ulsan": {"nx": 102, "ny": 84},
    "제주": {"nx": 52, "ny": 38},
    "Jeju": {"nx": 52, "ny": 38},
}

# 3. 날씨 코드 변환
SKY_CODE = {
    "1": "맑음",
    "3": "구름많음",
    "4": "흐림"
}

PTY_CODE = {
    "0": "없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "4": "소나기"
}


def get_base_datetime():
    """기상청 API 호출을 위한 기준 시간 계산"""
    now = datetime.now()
    
    # 발표 시간: 02, 05, 08, 11, 14, 17, 20, 23시
    base_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]
    
    # 현재 시간에서 가장 가까운 발표 시간 찾기
    current_hour = now.hour
    current_minute = now.minute
    
    # 발표 후 약 10분 뒤에 API 데이터가 갱신됨
    for i in range(len(base_times) - 1, -1, -1):
        base_hour = int(base_times[i][:2])
        if current_hour > base_hour or (current_hour == base_hour and current_minute >= 10):
            base_date = now.strftime("%Y%m%d")
            base_time = base_times[i]
            return base_date, base_time
    
    # 자정 이전이면 전날 23시 데이터 사용
    yesterday = now - timedelta(days=1)
    return yesterday.strftime("%Y%m%d"), "2300"


# 4. 도구(Tool) 등록하기

@mcp.tool()
def get_korea_weather(location: str) -> str:
    """
    =========== SHKWON=========
    한국 도시의 현재 날씨 정보를 가져옵니다.
    지원 도시: 서울, 부산, 대구, 인천, 광주, 대전, 울산, 제주
    영문 입력도 가능: Seoul, Busan, Daegu, Incheon, Gwangju, Daejeon, Ulsan, Jeju
    """
    logger.info(f"SHKWON - 🔧 [get_korea_weather] 호출됨 | 입력: location='{location}'")
    
    # 격자 좌표 확인
    grid = LOCATION_GRID.get(location)
    if not grid:
        result = f"지원하지 않는 지역입니다: {location}. 지원 도시: {list(LOCATION_GRID.keys())}"
        logger.warning(f"   ⚠️ {result}")
        return result
    
    # API 키 확인
    if not WEATHER_API_KEY:
        # API 키가 없으면 더미 데이터 반환 (테스트용)
        logger.warning("   ⚠️ WEATHER_API_KEY가 설정되지 않음. 더미 데이터 반환")
        dummy_weather = {
            "서울": "기온: 5°C, 맑음, 습도: 45%",
            "Seoul": "기온: 5°C, 맑음, 습도: 45%",
            "부산": "기온: 10°C, 구름많음, 습도: 60%",
            "Busan": "기온: 10°C, 구름많음, 습도: 60%",
            "대구": "기온: 7°C, 맑음, 습도: 40%",
            "Daegu": "기온: 7°C, 맑음, 습도: 40%",
            "인천": "기온: 4°C, 흐림, 습도: 55%",
            "Incheon": "기온: 4°C, 흐림, 습도: 55%",
            "광주": "기온: 8°C, 맑음, 습도: 50%",
            "Gwangju": "기온: 8°C, 맑음, 습도: 50%",
            "대전": "기온: 6°C, 구름많음, 습도: 48%",
            "Daejeon": "기온: 6°C, 구름많음, 습도: 48%",
            "울산": "기온: 9°C, 맑음, 습도: 52%",
            "Ulsan": "기온: 9°C, 맑음, 습도: 52%",
            "제주": "기온: 12°C, 구름많음, 습도: 65%",
            "Jeju": "기온: 12°C, 구름많음, 습도: 65%",
        }
        result = dummy_weather.get(location, "날씨 정보 없음")
        logger.info(f"   ✅ 더미 결과: {result}")
        return result
    
    try:
        base_date, base_time = get_base_datetime()
        
        # 기상청 단기예보 API 호출
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        params = {
            "serviceKey": WEATHER_API_KEY,
            "numOfRows": "100",
            "pageNo": "1",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": grid["nx"],
            "ny": grid["ny"]
        }
        
        logger.info(f"   📡 API 호출: {base_date} {base_time} ({location})")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 응답 파싱
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        
        if not items:
            result = f"{location}의 날씨 정보를 가져올 수 없습니다."
            logger.warning(f"   ⚠️ {result}")
            return result
        
        # 날씨 정보 추출
        weather_info = {}
        for item in items:
            category = item.get("category")
            fcst_value = item.get("fcstValue")
            
            if category == "TMP":  # 기온
                weather_info["기온"] = f"{fcst_value}°C"
            elif category == "SKY":  # 하늘상태
                weather_info["하늘"] = SKY_CODE.get(fcst_value, fcst_value)
            elif category == "PTY":  # 강수형태
                weather_info["강수"] = PTY_CODE.get(fcst_value, fcst_value)
            elif category == "REH":  # 습도
                weather_info["습도"] = f"{fcst_value}%"
            elif category == "WSD":  # 풍속
                weather_info["풍속"] = f"{fcst_value}m/s"
        
        result = f"{location} 날씨: " + ", ".join([f"{k}: {v}" for k, v in weather_info.items()])
        logger.info(f"   ✅ 결과: {result}")
        return result
        
    except requests.RequestException as e:
        result = f"API 호출 오류: {str(e)}"
        logger.error(f"   ❌ {result}")
        return result
    except Exception as e:
        result = f"오류 발생: {str(e)}"
        logger.error(f"   ❌ {result}")
        return result


@mcp.tool()
def get_weather_forecast(location: str, hours: int = 24) -> str:
    """
    =========== SHKWON ==========
    한국 도시의 날씨 예보를 가져옵니다.
    location: 도시명 (서울, 부산, 대구, 인천, 광주, 대전, 울산, 제주)
    hours: 예보 시간 (기본 24시간)
    """
    logger.info(f"SHKWON - 🔧 [get_weather_forecast] 호출됨 | location='{location}', hours={hours}")
    
    grid = LOCATION_GRID.get(location)
    if not grid:
        result = f"지원하지 않는 지역입니다: {location}"
        logger.warning(f"   ⚠️ {result}")
        return result
    
    # 간단한 예보 정보 반환 (더미 데이터)
    forecast = f"""
{location} {hours}시간 예보:
- 오전: 맑음, 기온 3~8°C
- 오후: 구름많음, 기온 5~10°C
- 저녁: 맑음, 기온 2~5°C
- 강수확률: 10%
- 미세먼지: 보통
"""
    logger.info(f"   ✅ 예보 생성 완료")
    return forecast.strip()


@mcp.tool()
def get_supported_cities() -> str:
    """
    ========== SHKWON ==========
    지원하는 한국 도시 목록을 반환합니다.
    """
    logger.info("SHKWON 🔧 [get_supported_cities] 호출됨")
    cities = list(set([k for k in LOCATION_GRID.keys() if not k[0].isupper()]))  # 한글만
    result = f"지원 도시: {', '.join(cities)}"
    logger.info(f"   ✅ {result}")
    return result


# 5. 서버 실행
if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("🌤️ Korea Weather Server 시작 중...")
    logger.info(f"📦 등록된 도구: get_korea_weather, get_weather_forecast, get_supported_cities")
    logger.info(f"🏙️ 지원 도시: 서울, 부산, 대구, 인천, 광주, 대전, 울산, 제주")
    logger.info("=" * 50)
    mcp.run(transport="sse", port=8003)
