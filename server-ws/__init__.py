"""WebSocket mirror of the gRPC services.

Keeps a single IRSDK connection (shared with telemetry/broadcast WS handlers).
"""
from irsdk import IRSDK
from .telemetry_ws import telemetry_router
from .broadcast_ws import broadcast_router

ir = IRSDK()               # shared instance – closes automatically on app shutdown

ROUTES = (
    ("/ws/telemetry", telemetry_router),
    ("/ws/broadcast", broadcast_router),
)
