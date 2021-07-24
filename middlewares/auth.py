import jwt
from functools import wraps
from flask import request, jsonify, abort
from modules.utils.token import get_info_from_token

def jwt_required(endpoint):

  @wraps(endpoint)
  def wrapper(*args, **kwargs):
    if not 'Authorization' in request.headers:
      abort(401, 'token required')
    else:
      try:
        auth_header = request.headers['Authorization'].split('Bearer ')[1]
        get_info_from_token(auth_header)
        return endpoint(*args, **kwargs)
      except jwt.ExpiredSignatureError:
        abort(403, 'token expired')
      except jwt.DecodeError:
        abort(400, 'invalid token')
  
  return wrapper