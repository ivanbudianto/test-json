# third-party imports
from flask import Flask, jsonify
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# local imports
from .config import DevelopmentConfig


api = Api()
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

authorizations = {
  "jsonWebToken": {
    "type": "apiKey",
    "in": "header",
    "name": "Authorization"
  }
}

def create_app(config=DevelopmentConfig):
  app = Flask(__name__)
  app.config.from_object(config)

  api.init_app(app, version="1.0", title="Back-End Engineer Test API", description="Recruitment Test Back-End Engineer CDP 2023")
  db.init_app(app)
  bcrypt.init_app(app)
  jwt.init_app(app)

  from .resources import auth_ns, data_ns
  api.add_namespace(auth_ns)
  api.add_namespace(data_ns)

  from .models import User
  @jwt.unauthorized_loader
  def custom_error_message(callback):
    return jsonify({"message": "Unauthorized access"}), 401

  @jwt.user_identity_loader
  def user_identity_lookup(user):
    return user.id

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

  with app.app_context():
    db.create_all()

  return app