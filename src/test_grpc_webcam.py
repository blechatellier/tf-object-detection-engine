import grpc
import os
import cv2
import random
import numpy as np
from config import config
import grpc_pb2
import grpc_pb2_grpc

WIDTH = 640
HEIGHT = 480

def main():
  channel = grpc.insecure_channel(config['host'] + ':' + str(config['grpc_port']))
  stub = grpc_pb2_grpc.GrpcStub(channel)

  stream = cv2.VideoCapture(0)
  stream.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
  stream.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
  colors = {}

  while True:
    (grabbed, frame) = stream.read()
    image_data = cv2.imencode('.jpg', frame)[1].tostring()
    response = stub.Detect(grpc_pb2.Image(data=image_data))

    for prediction in response.prediction:
      if prediction.label in colors:
        pass
      else:
        colors[prediction.label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

      color = colors[prediction.label]

      x1 = int(prediction.box.left * WIDTH)
      y1 = int(prediction.box.top * HEIGHT)
      x2 = int(prediction.box.right * WIDTH)
      y2 = int(prediction.box.bottom * HEIGHT)
      text = prediction.label + ': ' + str(int(prediction.score * 100)) + '%'

      cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
      cv2.putText(frame, text, (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, .5, color)
    
    cv2.imshow('Engine', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
