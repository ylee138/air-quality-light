import asyncio
import requests
from pywizlight import wizlight, PilotBuilder

# --- Configuration (REPLACE WITH YOUR OWN DATA) ---
TOKEN = "YOUR_API_TOKEN_HERE"  # Obtain from aqicn.org/api/
CITY = "seoul"                 # Target city for AQI monitoring
BULB_IP = "192.168.x.x"        # Local IP address of your WiZ bulb

async def main():
    # Attempting to connect to the smart bulb
    light = wizlight(BULB_IP)
    print(f"System Initialized: Connecting to bulb at {BULB_IP}...")

    while True:
        try:
            # 1. Fetch real-time air quality data (WAQI API)
            url = f"https://api.waqi.info/feed/{CITY}/?token={TOKEN}"
            response = requests.get(url).json()
            
            if response['status'] == 'ok':
                aqi = response['data']['aqi']
                print(f"Current {CITY} AQI Index: {aqi}")

                # 2. Determine color mapping based on AQI levels
                if aqi <= 50:
                    # Healthy: Blue
                    rgb = (0, 0, 255)
                    status = "Healthy (Blue)"
                elif aqi <= 100:
                    # Moderate: Green
                    rgb = (0, 255, 0)
                    status = "Moderate (Green)"
                elif aqi <= 150:
                    # Unhealthy: Orange
                    rgb = (255, 165, 0)
                    status = "Unhealthy (Orange)"
                else:
                    # Hazardous: Red
                    rgb = (255, 0, 0)
                    status = "Hazardous (Red)"

                # 3. Transmit spectral command to the bulb
                print(f"Updating bulb state -> {status}")
                await light.turn_on(PilotBuilder(rgb=rgb, brightness=255))
            else:
                print("Failed to retrieve API data.")
            
        except Exception as e:
            print(f"Error occurred: {e}. Check network connectivity.")

        # Wait for 10 minutes (600 seconds) before the next update
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())