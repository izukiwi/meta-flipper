import asyncio
import hashlib
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from bleak import BleakScanner

TARGET_MANUFACTURERS = {
    0x0D53: "Ray-Ban Meta (Luxottica)",
    0x01AB: "Meta Platforms"
}

# Gestionnaire de connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                pass

manager = ConnectionManager()
scanner_loop = None

def get_stable_angle(address: str) -> float:
    """Génère un angle fixe (0-360°) dérivé de l'adresse MAC."""
    digest = hashlib.md5(address.encode()).hexdigest()
    return (int(digest[:4], 16) % 360)

def on_device_detected(device, adv_data):
    for comp_id, brand in TARGET_MANUFACTURERS.items():
        if comp_id in adv_data.manufacturer_data:
            # Modèle de perte de propagation log-distance (n=2, RSSI à 1 m = -65 dBm)
            distance = round(10 ** ((-65 - adv_data.rssi) / (10 * 2)), 1)
            distance = min(distance, 15.0)  # Plafond à 15 mètres

            payload = {
                "address": device.address,
                "brand": brand,
                "rssi": adv_data.rssi,
                "distance": distance,
                "angle": get_stable_angle(device.address),
                "timestamp": datetime.now().isoformat()
            }
            # Transmission asynchrone sur la boucle d'événements
            asyncio.run_coroutine_threadsafe(manager.broadcast(payload), scanner_loop)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global scanner_loop
    scanner_loop = asyncio.get_running_loop()
    scanner = BleakScanner(detection_callback=on_device_detected)
    await scanner.start()
    yield
    await scanner.stop()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)