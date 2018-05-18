import os
from dotenv import load_dotenv

load_dotenv()

config = {
  'host': os.getenv('HOST') or '0.0.0.0',
  'grpc_port': int(os.getenv('GRPC_PORT')) if os.getenv('GRPC_PORT') else 50051,
  'http_port': int(os.getenv('HTTP_PORT')) if os.getenv('HTTP_PORT') else 3000,
  'threshold': float(os.getenv('THRESHOLD')) if os.getenv('THRESHOLD') else 0.5,
  'model': os.getenv('MODEL') or 'ssd_inception_v2_coco_2017_11_17',
}