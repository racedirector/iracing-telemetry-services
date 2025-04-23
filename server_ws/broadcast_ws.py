import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.broadcast_service import BroadcastService        # reuse logic  [oai_citation_attribution:1‡GitHub](https://github.com/racedirector/iracing-telemetry-grpc/blob/main/server/broadcast_service.py)
from server_ws import ir

router = APIRouter()
svc = BroadcastService(ir)   # thin wrapper around IRSDK – stateful

# Map JSON "action" -> method on BroadcastService
_ACTION_TABLE = {
    fn.lower(): fn
    for fn in dir(BroadcastService)
    if not fn.startswith("_")
}

@router.websocket("")
async def broadcast_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            req = json.loads(raw)
            action = req.pop("action", "").lower()
            fn_name = _ACTION_TABLE.get(action)
            if not fn_name:
                await ws.send_json({"error": f"unknown action '{action}'"})
                continue

            # call the gRPC‑style method with keyword params unpacked from JSON
            method = getattr(svc, fn_name)
            try:
                result = method(**req)  # pylint: disable=*args‑differ
                await ws.send_json({"result": result})  # pydantic encodes protobuf OK
            except Exception as exc:  # noqa: BLE001
                await ws.send_json({"error": str(exc)})
    except WebSocketDisconnect:
        return
