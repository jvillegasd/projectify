from functools import wraps
from flask import request, jsonify, abort

def parameters(schema, upload_file=False):

  def decorator(endpoint):

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
      body = request.get_json() or dict()

      if 'file' in request.files:
        body['filename'] = request.files['file'].filename
      
      errors = schema.validate(body)
      if errors:
        abort(400, str(errors))
      else:
        return endpoint(*args, **kwargs)
    
    return wrapper
  
  return decorator
