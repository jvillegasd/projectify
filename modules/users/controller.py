from flask import request, Blueprint

user_blueprint = Blueprint("User controller", __name__)

@user_blueprint.route("/", methods=["POST"])
def create():
   
  return 