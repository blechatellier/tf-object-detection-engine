import logging
import threading
from config import config
from engine import Engine
from grpc_server import GrpcServer
from http_server import HttpServer

def main():
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  engine = Engine(config)
  
  grpc_server = threading.Thread(target=GrpcServer, args=[config, engine])
  grpc_server.start()
  logging.info('Grpc server started at %s:%s', config['host'], config['grpc_port'])

  http_server = threading.Thread(target=HttpServer, args=[config, engine])
  http_server.start()
  logging.info('HTTP server started at %s:%s', config['host'], config['http_port'])
  
if __name__ == '__main__':
  main()