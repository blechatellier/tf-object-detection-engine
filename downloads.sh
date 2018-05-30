mkdir -p src/models
curl http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2017_11_17.tar.gz | tar -xz -C src/models
curl -o src/models/mscoco_label_map.pbtxt https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt