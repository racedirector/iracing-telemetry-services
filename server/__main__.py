import logging
from server.server import Server

if __name__ == "__main__":
  logging.basicConfig()
  server = Server()

  try:
    server.start()
  except KeyboardInterrupt:
    server.stop()