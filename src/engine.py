import logging
import os
import datetime
import cv2
import numpy as np
import tensorflow as tf

class Engine:
  MODELS_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../models'

  def __init__(self, config):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    self.config = config
    self.sess = tf.Session()
    self.labels = self.load_labels(Engine.MODELS_PATH + '/mscoco_label_map.pbtxt')
    self.load_model(Engine.MODELS_PATH + '/' + self.config['model'] +'/frozen_inference_graph.pb')

    logging.info('Engine initialized')

  def load_model(self, model_file):
    logging.info('Loading engine model %s', self.config['model'])

    with tf.gfile.FastGFile(model_file, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

  @staticmethod
  def load_labels(labels_file):
    logging.info('Loading engine labels')

    labels = {}
    label_lines = tf.gfile.GFile(labels_file).readlines()
    for line in label_lines:
      if line.startswith('  id:'):
        id = int(line.split(': ')[1])
      if line.startswith('  display_name:'):
        display_name = line.split(': ')[1]
        labels[id] = display_name[1:-2]

    return labels
  
  @staticmethod
  def getElapsedTime(start_time):
    return '{0:.3f}'.format((datetime.datetime.now() - start_time).total_seconds())

  def predict(self, image_data):
    start_time = datetime.datetime.now()

    image_tensor = self.sess.graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = self.sess.graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = self.sess.graph.get_tensor_by_name('detection_scores:0')
    detection_classes = self.sess.graph.get_tensor_by_name('detection_classes:0')

    nparr = np.fromstring(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    image_np_expanded = np.expand_dims(image, axis=0)

    (boxes, scores, classes) = self.sess.run([detection_boxes, detection_scores, detection_classes], feed_dict={image_tensor: image_np_expanded})

    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)
    classes = np.squeeze(classes).astype(np.int32)

    results = []
    for i in range(len(classes)):
      result = {}
      top, left, bottom, right = boxes[i]
      result['label'] = self.labels[classes[i]]
      result['score'] = float(scores[i])
      result['box'] = {'top': float(top), 'left': float(left), 'bottom': float(bottom), 'right': float(right)}

      if result['score'] > self.config['threshold']:
        results.append(result)
    
    logging.info('Finished engine prediction +%ss', Engine.getElapsedTime(start_time))

    return results