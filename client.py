"""Python implementation of the GRPC sensor client."""
from __future__ import print_function
import sys
import os

# 👇 Add this BEFORE importing sensor_pb2
proto_dir = os.path.join(os.path.dirname(__file__), 'proto')
sys.path.insert(0, proto_dir)

import logging
import asyncio
import grpc
from dotenv import load_dotenv
from proto import telemetry_pb2
from proto import telemetry_pb2_grpc

load_dotenv()

class Environment:
  host = os.getenv("HOST")
  port = os.getenv("PORT")
  fps = int(os.getenv("FPS"))

  @classmethod
  def api_url(cls):
    return cls.host + ":" + cls.port

async def run() -> None:
  async with grpc.aio.insecure_channel(Environment.api_url()) as channel:
    stub = telemetry_pb2_grpc.TelemetryStub(channel)

    # Direct read from the stub
    telemetry_stream = stub.SubscribeTelemetry(
      telemetry_pb2.TelemetrySubscriptionRequest(fps=Environment.fps, keys=["CarIdxLapDistPct"])
    )

    while True:
      response = await telemetry_stream.read()
      if response == grpc.aio.EOF:
        break


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
