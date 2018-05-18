# Engine

### Install dependencies
```
pip install virtualenv
virtualenv venv --python=python3.6
venv/bin/pip install -r requirements.txt
```

> Also install requirements.cpu.txt or requirements.gpu.txt depending on your hardware setup.

### Download model and labels
```
./downloads.sh
```

> More coco models available for [download](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md).

### Genetate protos
```
venv/bin/python -m grpc_tools.protoc -I protos --python_out=src --grpc_python_out=src protos/grpc.proto
```

### Run servers
```
venv/bin/python src/main.py
```

### Run test
```
venv/bin/python src/test_grpc.py src/test.jpg
venv/bin/python src/test_grpc_webcam.py
```