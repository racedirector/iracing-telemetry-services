import logging, os
from server.server import Server

if __name__ == "__main__":
  logging.basicConfig()
  server = Server(port=int(os.getenv("PORT", 50051)))

  try:
    server.start()
  except KeyboardInterrupt:
    server.stop()