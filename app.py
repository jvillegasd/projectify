from environs import Env
from flask_cors import CORS
from flask import Flask, jsonify, json
from werkzeug.exceptions import HTTPException

from modules import user_blueprint, project_blueprint, report_blueprint

env = Env()
env.read_env()

app = Flask(__name__)

# Limiting file size
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 # 3mb

# Validating file extensions
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx', '.xls', '.csv']

# CORS for frontend application
CORS(app, resources={r"/*": {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Add blueprints to main app
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(project_blueprint, url_prefix='/projects')
app.register_blueprint(report_blueprint, url_prefix='/reports')

# Ping
@app.route('/')
def ping():
  return jsonify({'message': 'server is up!'}), 200

# Error handling to json
@app.errorhandler(HTTPException)
def handle_exception(e):
  response = e.get_response()
  response.data = json.dumps({
    'code': e.code,
    'name': e.name,
    'description': e.description,
  })
  response.content_type = 'application/json'
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=env('FLASK_PORT'), debug=True)
