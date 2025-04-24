import argparse
from asyncio import sleep
import os
import uvicorn
import yaml
import json as jsonlib
from iracing.date_encoder import DateEncoder
from typing import List
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from iracing.iracing_service import IRacingService
from pathlib import Path

test_file = os.getenv("PYIRSDK_TEST_FILE", None)

client = IRacingService(
    test_file=test_file
)

app = FastAPI(title="iRacing Telemetry API", debug=True)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse(static_dir / "index.html")

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

@app.get("/dump", response_class=Response, responses={ 
    200: { 
        "description": "Dump of telemetry data in YML format"
    }
})
def dump(json: bool = Query(False, description="Return the dump as JSON"), include_session: bool = Query(False, alias="includeSession", description="Include session data in the dump")):
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    telemetry_dump = client.dump_telemetry()

    if include_session:
        session_string = client.get_session_string()
        session_json = yaml.safe_load(session_string)
        telemetry_dump.update(session_json)

    if json:
        return Response(content=jsonlib.dumps(telemetry_dump, default=DateEncoder), media_type="application/json")
    else:
        return Response(content=yaml.dump(telemetry_dump), media_type="application/x-yaml")
    

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
    if fps <= 0 or fps > 60:
        raise HTTPException(status_code=400, detail="FPS must be greater than 0 and less than or equal to 60")

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

if __name__ == "__main__":  # pragma: no cover
    # multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description="iRacing HTTP server")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--test", type=Path,
                    help="Pass a .bin telemetry file for offline testing")
    
    args = parser.parse_args()

    if args.test is not None:
        import os
        os.environ["PYIRSDK_TEST_FILE"] = str(args.test)

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    