import asyncio
import requests
from pywizlight import wizlight, PilotBuilder

# --- 개인 설정 부분 ---
TOKEN = "c987c48d13943cf15ba41b2bfc6d0a1417b97730"
CITY = "seoul"  # 뉴질랜드 도시로 바꾸려면 "auckland" 등으로 수정 가능합니다
BULB_IP = "192.168.1.75" 

async def main():
    # 전구와 연결 시도
    light = wizlight(BULB_IP)
    print(f"시스템 시작: 전구({BULB_IP}) 연결 중...")

    while True:
        try:
            # 1. 미세먼지 정보 가져오기 (WAQI API)
            url = f"https://api.waqi.info/feed/{CITY}/?token={TOKEN}"
            response = requests.get(url).json()
            
            if response['status'] == 'ok':
                aqi = response['data']['aqi']
                print(f"현재 {CITY} AQI 지수: {aqi}")

                # 2. AQI 수치에 따른 색상 설정
                if aqi <= 50:
                    # 좋음: 파란색
                    rgb = (0, 0, 255)
                    status = "좋음 (Blue)"
                elif aqi <= 100:
                    # 보통: 초록색
                    rgb = (0, 255, 0)
                    status = "보통 (Green)"
                elif aqi <= 150:
                    # 나쁨: 주황색
                    rgb = (255, 165, 0)
                    status = "나쁨 (Orange)"
                else:
                    # 매우 나쁨: 빨간색
                    rgb = (255, 0, 0)
                    status = "매우 나쁨 (Red)"

                # 3. 전구 색상 변경 명령
                print(f"전구 상태 변경 중 -> {status}")
                await light.turn_on(PilotBuilder(rgb=rgb, brightness=255))
            else:
                print("API 데이터를 가져오는데 실패했습니다.")
            
        except Exception as e:
            print(f"에러 발생: {e}. 전구 IP나 와이파이 연결을 확인하세요.")

        # 10분(600초) 대기 후 다시 확인
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())