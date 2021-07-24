from environs import Env
from flask_cors import CORS
from flask import Flask, jsonify

from modules.users.controller import user_blueprint

env = Env()
env.read_env()

app = Flask(__name__)

# CORS for frontend application
CORS(app, resources={r"/*": {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(user_blueprint, url_prefix='/users')

# Ping
@app.route('/')
def ping():
  return jsonify({'message': 'server is up!'}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=env('FLASK_PORT'), debug=True)
