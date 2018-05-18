import grpc
import os
import sys
import cv2
import random
from config import config
import grpc_pb2
import grpc_pb2_grpc

def main(argv):
  if not argv:
    print('Missing image file argument')
    sys.exit()

  channel = grpc.insecure_channel(config['host'] + ':' + str(config['grpc_port']))
  stub = grpc_pb2_grpc.GrpcStub(channel)

  print('Sending requests to Engine')
  frame = cv2.imread(argv[0])
  image_data = cv2.imencode('.jpg', frame)[1].tostring()
  response = stub.Detect(grpc_pb2.Image(data=image_data))
  frame_width = frame.shape[1]
  frame_height = frame.shape[0]

  colors = {}
  for prediction in response.prediction:
    if prediction.label in colors:
      pass
    else:
      colors[prediction.label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    color = colors[prediction.label]

    x1 = int(prediction.box.left * frame_width)
    y1 = int(prediction.box.top * frame_height)
    x2 = int(prediction.box.right * frame_width)
    y2 = int(prediction.box.bottom * frame_height)
    text = prediction.label + ': ' + str(int(prediction.score * 100)) + '%'

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, text, (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, .5, color)
  
  cv2.imshow('Engine', frame)
  cv2.waitKey(0)

if __name__ == '__main__':
  main(sys.argv[1:])
