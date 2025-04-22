import json, asyncio
from typing import Dict, List, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.telemetry_service import (
    get_telemetry_from_iracing,   # ↩ reuse existing helper  [oai_citation_attribution:0‡GitHub](https://github.com/racedirector/iracing-telemetry-grpc/blob/main/server/telemetry_service.py)
)
from server_ws import ir

router = APIRouter()

async def _send_periodic(
    websocket: WebSocket, keys: List[str], fps: int
) -> None:
    cache: Dict[str, Any] = {}
    frame_time = 1 / fps
    while True:
        if not (ir.is_initialized and ir.is_connected):
            await websocket.send_json({"error": "iRacing disconnected"})
            break
        data = get_telemetry_from_iracing(ir, keys,
                                          lambda k: k not in cache or cache[k] != ir[k])
        if data:
            cache.update(data)
            await websocket.send_json({"telemetry": data})
        await asyncio.sleep(frame_time)

@router.websocket("")      # full path injected by __init__.py
async def telemetry_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            req = json.loads(msg)
            action = req.get("action")
            keys = req.get("keys", [])
            if action == "get":
                await websocket.send_json(
                    {"telemetry": get_telemetry_from_iracing(ir, keys)}
                )
            elif action == "subscribe":
                fps = max(1, min(int(req.get("fps", 1)), 60))
                await websocket.send_json({"status": f"subscribed @ {fps} fps"})
                await _send_periodic(websocket, keys, fps)
            else:
                await websocket.send_json(
                    {"error": "unknown action; use 'get' or 'subscribe'"}
                )
    except WebSocketDisconnect:
        return
