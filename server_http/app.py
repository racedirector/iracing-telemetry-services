import os
from typing import List
from fastapi import FastAPI, HTTPException, Query
from iracing.iracing_service import IRacingService

client = IRacingService(
    test_file=os.getenv("PYIRSDK_TEST_FILE", None),
)

app = FastAPI(title="iRacing Telemetry REST API", debug=True)

@app.get("/telemetry")
def telemetry(keys: List[str] = Query(..., description="List of telemetry keys to retrieve")):
    if not keys:
        raise HTTPException(status_code=400, detail="No keys provided")
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    telemetry_data = client.get_telemetry(keys)
    if not telemetry_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve telemetry data")
    return telemetry_data

@app.get("/schema")
def json_schema():
    """
    Returns the telemetry schema.
    """
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    return {
        "telemetry": client.telemetry_schema,
        "session": client.session_schema
    }

@app.get("/schema/telemetry")
def telemetry_schema():
    """
    Returns the telemetry schema.
    """
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    return client.telemetry_schema

@app.get("/schema/session")
def session_schema():
    """
    Returns the session schema.
    """
    if not client.check_connection():
        raise HTTPException(status_code=503, detail="iRacing client is not connected")
    
    return client.session_schema