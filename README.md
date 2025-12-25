# air-quality-light
This project translates real-time air quality data (AQI) from Seoul into physical light 
spectrum in Auckland, NZ, using a Raspberry Pi Zero 2 W and a WiZ Smart Bulb. 

## Materials
- Hardware: Raspberry Pi Zero 2 W, WiZ Tunable White & Color Bulb (E27)
- Data Source: World Air Quality Index (WAQI) API

## How to use
1. Install requirements: `pip install requests pywizlight asyncio`
2. Update the `BULB_IP` and `TOKEN` in `air_monitor.py`.
3. Deploy the `.service` file to `/etc/systemd/system/` for 24/7 automation.
