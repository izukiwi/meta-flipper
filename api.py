import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

import meta_detector

# Mémoire cache des cibles Meta détectées
targets = {}
TTL_SECONDS = 10.0

def detection_callback(device: BLEDevice, adv: AdvertisementData):
    meta_info = meta_detector.analyze_device(device, adv)
    if meta_info:
        meta_info["last_seen"] = time.time()
        targets[device.address] = meta_info

async def ble_scanner_task():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(1)
            # Nettoyage des cibles perdues
            now = time.time()
            expired = [k for k, v in targets.items() if now - v["last_seen"] > TTL_SECONDS]
            for k in expired:
                del targets[k]
    finally:
        await scanner.stop()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(ble_scanner_task())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/targets")
def get_targets():
    return list(targets.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)