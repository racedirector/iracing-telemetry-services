from asyncio import sleep
import os
from . import make_mock_open, CaptureOnCloseBuffer
from typing import List
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.websockets import WebSocket
from iracing.iracing_service import IRacingService
from unittest.mock import patch
from pathlib import Path

test_file = os.getenv("PYIRSDK_TEST_FILE", None)

client = IRacingService(
    test_file=test_file
)

app = FastAPI(title="iRacing Telemetry API", debug=True)

@app.get("/telemetry", responses={
    200: {
        "content": { "application/json": { "example": { "PlayerCarIdx": 18, "LapDistPct": 0 }}},
        "description": "Telemetry data"
    }
})
def telemetry(keys: List[str] = Query(..., description="List of telemetry keys to retrieve", example=["PlayerCarIdx", "LapDistPct"])):
    if not keys:
        raise HTTPException(status_code=400, detail="No keys provided")
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    telemetry_data = client.get_telemetry(keys)
    if not telemetry_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve telemetry data")
    return telemetry_data

dump_path = Path(__file__).parent / "dump_response.yml"

@app.get("/dump", response_class=Response, responses={ 
    200: { 
        "content": { "application/x-yaml": { "example": dump_path.read_text() }},
        "description": "Dump of telemetry data in YML format"
    }
})
def dump():
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    request_buffer = CaptureOnCloseBuffer()
    with patch("builtins.open", make_mock_open(request_buffer)):
        client.client.parse_to('dump_path')

    return request_buffer.getvalue()
    

@app.websocket("/ws/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for telemetry data.
    """
    await websocket.accept()
    connect_message = await websocket.receive_json()
    fps = connect_message["fps"]
    keys = connect_message["keys"]
    if not keys:
        raise HTTPException(status_code=400, detail="No keys provided")
    if not fps:
        raise HTTPException(status_code=400, detail="No fps provided")
    if fps < 1 or fps > 60:
        raise HTTPException(status_code=400, detail="FPS must be between 1 and 60")

    with IRacingService(test_file=test_file) as iracing_service:
        while iracing_service.check_connection():
            telemetry_data = iracing_service.get_telemetry(keys)
            if telemetry_data:
                await websocket.send_json(telemetry_data)
            else:
                await websocket.send_json({"error": "Failed to retrieve telemetry data"})
            
            # Sleep for the specified FPS
            await sleep(1 / fps)

        await websocket.close()

@app.get("/schema/telemetry", responses={
    200: {
        "description": "Telemetry JSON schema"
    }
})
def telemetry_schema():
    """
    Returns the telemetry schema.
    """
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    return client.telemetry_schema

@app.get("/schema/session", responses={
    200: {
        "description": "Session JSON schema"
    }   
})
def session_schema():
    """
    Returns the session schema.
    """
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    return client.session_schema