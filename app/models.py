# third-party imports
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# local imports
from . import db


class User(db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), nullable=False)
  username = db.Column(db.String(20), nullable=False, unique=True)
  email = db.Column(db.String(128), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  token = db.Column(db.String(300), nullable=True)
  reset_token = db.Column(db.String(300), nullable=True)
  datas = db.relationship("Data", back_populates="user")

  def get_reset_token(self, expires_sec=1800):
    serial = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    return serial.dumps({"user_id": self.id}).decode("utf-8")

  @staticmethod
  def verify_reset_token(token):
    serial = Serializer(current_app.config["SECRET_KEY"])
    try:
      user_id = serial.loads(token)["user_id"]
    except:
      return None
    return User.query.get(user_id)

  def __repr__(self):
    return f"<User: {self.username}>"

class Data(db.Model):
  __tablename__ = "data"

  id = db.Column(db.Integer, primary_key=True)
  source = db.Column(db.String(60), nullable=False)
  sentiment = db.Column(db.String(60), nullable=False)
  text = db.Column(db.Text, nullable=False)
  created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  user = db.relationship("User", back_populates="datas")

  def __repr__(self):
    return f"<Data: {self.text}>"