from functools import wraps
from flask import request, jsonify, abort

def parameters(schema):

  def decorator(endpoint):

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
      errors = schema.validate(request.get_json())
      if errors:
        abort(400, str(errors))
      else:
        return endpoint(*args, **kwargs)
    
    return wrapper
  
  return decorator
