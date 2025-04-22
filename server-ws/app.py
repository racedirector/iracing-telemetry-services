from fastapi import FastAPI
from . import ROUTES, ir

app = FastAPI(title="iRacing Telemetry WS")

# register WS routes
for path, router in ROUTES:
    app.include_router(router, prefix=path)

@app.on_event("startup")
def _connect():
    if not (ir.is_initialized and ir.is_connected):
        ir.startup()

@app.on_event("shutdown")
def _disconnect():
    if ir.is_connected:
        ir.shutdown()
