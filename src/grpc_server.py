import logging
import time
import grpc
import grpc_pb2
import grpc_pb2_grpc
from concurrent import futures

class GrpcServicer(grpc_pb2_grpc.GrpcServicer):
  def __init__(self, engine):
    self.engine = engine

  def Detect(self, request, context):
    return grpc_pb2.Predictions(prediction=self.engine.predict(request.data))

class GrpcServer:
  def __init__(self, config, engine):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_GrpcServicer_to_server(GrpcServicer(engine), server)
    server.add_insecure_port(config['host'] + ':' + str(config['grpc_port']))
    server.start()
    
    try:
      while True:
        time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
      server.stop(0)