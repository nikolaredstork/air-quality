from fastapi import FastAPI, WebSocket
import requests
import asyncio
from fastapi.middleware.cors import CORSMiddleware

# FastAPI App
app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "3B5BD903-FB9F-11EF-A3B4-42010A800010"  # Replace with your API key
SENSOR_ID = "122201"  # Replace with the actual sensor ID

# Fetch AQI Data from PurpleAir API
# Fetch AQI Data from PurpleAir API
def get_aqi():
    url = f"https://api.purpleair.com/v1/sensors/{SENSOR_ID}"
    headers = {
        "X-API-Key": API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)

        data = response.json()
        if "sensor" in data and "pm2.5" in data["sensor"]:
            pm25 = data["sensor"]["pm2.5"]
            return {"pm2.5": pm25, "aqi": calculate_aqi(pm25)}

        return {"error": "Invalid response format"}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}


# Function to Convert PM2.5 to AQI (Using EPA Standard)
def calculate_aqi(pm25):
    if pm25 is None:
        return None
    
    if pm25 <= 12.0:
        return round((50 / 12) * pm25)
    elif pm25 <= 35.4:
        return round(((100 - 51) / (35.4 - 12.1)) * (pm25 - 12.1) + 51)
    elif pm25 <= 55.4:
        return round(((150 - 101) / (55.4 - 35.5)) * (pm25 - 35.5) + 101)
    elif pm25 <= 150.4:
        return round(((200 - 151) / (150.4 - 55.5)) * (pm25 - 55.5) + 151)
    elif pm25 <= 250.4:
        return round(((300 - 201) / (250.4 - 150.5)) * (pm25 - 150.5) + 201)
    elif pm25 <= 350.4:
        return round(((400 - 301) / (350.4 - 250.5)) * (pm25 - 250.5) + 301)
    elif pm25 <= 500.4:
        return round(((500 - 401) / (500.4 - 350.5)) * (pm25 - 350.5) + 401)
    else:
        return 500  # Beyond max AQI range

# Endpoint for REST API polling
@app.get("/aqi")
def read_aqi():
    return get_aqi()

# WebSocket Connection for real-time AQI updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        aqi_data = get_aqi()
        await websocket.send_json(aqi_data)
        await asyncio.sleep(30)  # Send update every 30 seconds
