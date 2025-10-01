from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import threading
import os

# NOTE: OLA Python binding becomes available when OLA is installed via your OS (e.g. apt install ola).
try:
    import ola.ClientWrapper
    _OLA_AVAILABLE = True
except Exception as _e:
    _OLA_AVAILABLE = False
    ola = None

app = FastAPI(title="Theater DMX Server", version="1.0.0")

# --- Static frontend mount ---
# Absoluten Pfad ermitteln: /pfad/zu/deinem/projekt/frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# optional CORS aktivieren, falls JS fetcht
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder nur ["http://localhost"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/__debug_routes")
def debug_routes():
    return [f"{r.path} → {','.join(r.methods)}" for r in app.routes]
# statische Dateien mounten


# --- DMX Setup ---
UNIVERSE = 0
DMX_LOCK = threading.Lock()
DMX_BUFFER = bytearray([0] * 512)

wrapper = None
client = None
if _OLA_AVAILABLE:
    wrapper = ola.ClientWrapper.ClientWrapper()
    client = wrapper.Client()

class ChannelValue(BaseModel):
    address: int  # 1..512
    value: int    # 0..255

class DMXPayload(BaseModel):
    channels: List[ChannelValue]

@app.post("/api/dmx")
def set_dmx(payload: DMXPayload):
    """Set one or more DMX channel values (1..512)."""
    updated = 0
    with DMX_LOCK:
        for ch in payload.channels:
            if 1 <= ch.address <= 512:
                DMX_BUFFER[ch.address - 1] = max(0, min(255, int(ch.value)))
                updated += 1
        if _OLA_AVAILABLE and client:
            client.SendDmx(UNIVERSE, DMX_BUFFER)
    return {"status": "ok", "updated": updated}

@app.post("/api/scene")
def set_scene(scene: dict):
    """Apply a full DMX frame: { "dmx": [0..255 x up to 512] }"""
    arr = scene.get("dmx")
    if not isinstance(arr, list) or len(arr) == 0:
        return {"status": "error", "message": "missing 'dmx' array"}
    with DMX_LOCK:
        for i, v in enumerate(arr[:512]):
            DMX_BUFFER[i] = max(0, min(255, int(v)))
        if _OLA_AVAILABLE and client:
            client.SendDmx(UNIVERSE, DMX_BUFFER)
    return {"status": "ok", "applied": min(len(arr), 512)}

@app.get("/api/status")
def status():
    return {
        "universe": UNIVERSE,
        "ola_available": _OLA_AVAILABLE,
        "preview_first_24_channels": list(DMX_BUFFER[:24]),
    }
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")