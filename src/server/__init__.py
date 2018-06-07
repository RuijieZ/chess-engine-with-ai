from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_file(path):
	return send_from_directory('static', path)