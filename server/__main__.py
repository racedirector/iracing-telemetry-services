import argparse
import logging, os
from irsdk import IRSDK
from server.server import Server

VERSION = '0.0.1'

def main(
    port=os.getenv("PORT", 50051),
    test_file=None):
  logging.basicConfig()

  iracing = IRSDK()
  if (test_file is not None):
    print("Starting iRacing with test file: %s" % test_file)  
    iracing.startup(test_file=test_file)

  server = Server(
    port=int(port),
    iracing=iracing,
  )

  try:
    server.start()
  except KeyboardInterrupt:
    server.stop()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="iRacing gRPC server")
  parser.add_argument('-v', '--version', action='version', version='Python iRacing gRPC %s' % VERSION, help='show version and exit')
  parser.add_argument('-p', '--port', help='port to listen on (default: 50051)', default=os.getenv("PORT", 50051))
  parser.add_argument('--test', help='use test file as irsdk mmap')
  args = parser.parse_args()

  main(test_file=args.test)