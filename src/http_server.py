import logging
from http import HTTPStatus
from flask import Flask, request, jsonify
from flask_cors import CORS

class HttpServer:
  def __init__(self, config, engine):
    logger = logging.getLogger('werkzeug')
    logger.disabled = True

    self.engine = engine

    server = Flask(__name__)
    CORS(server)
    server.route('/detect', methods=['POST'])(self.detect)
    server.run(host=config['host'], port=config['http_port'], threaded=True)    

  @staticmethod
  def bad_request(message):
    return jsonify({ 'error': { 'type': 'badRequest', 'message': message } }), HTTPStatus.BAD_REQUEST

  def detect(self):
    if 'image' not in request.files:
      return HttpServer.bad_request('Missing image file')

    return jsonify(self.engine.predict(request.files['image'].read()))
