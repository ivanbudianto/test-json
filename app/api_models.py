# third-party imports
from flask_restx import fields

# local imports
from . import api


register_response_model = api.model("Register Response", {
  "id": fields.Integer(description="ID"),
  "name": fields.String(description="Name"),
  "username": fields.String(description="Username"),
  "email": fields.String(description="Email"),
  "created_date": fields.DateTime(description="Created Date")
})

login_response_model = api.model("Login Response", {
  "token": fields.String(description="Token")
})

forgot_password_response_model = api.model("Forgot Password Response", {
  "reset_token": fields.String(description="Reset Token")
})

data_response_model = api.model("Data Response", {
  "id": fields.Integer(description="ID"),
  "source": fields.String(description="Source"),
  "sentiment": fields.String(description="Sentiment"),
  "text": fields.String(description="Text"),
  "created_date": fields.DateTime(description="Created Date"),
  "user": fields.Nested(api.model("Nested User", {
    "id": fields.Integer(description="ID"),
    "username": fields.String(description="Username")
  }))
})

register_model = api.model("Register", {
  "name": fields.String(required=True, description="Name"),
  "username": fields.String(required=True, description="Username"),
  "email": fields.String(required=True, description="Email"),
  "password": fields.String(required=True, description="Password")
})

login_model = api.model("Login", {
  "username": fields.String(required=True, description="Username"),
  "password": fields.String(required=True, description="Password")
})

change_password_model = api.model("Change Password", {
  "current_password": fields.String(required=True, description="Current Password"),
  "new_password": fields.String(required=True, description="New Password")
})

forgot_password_model = api.model("Forgot Password", {
  "email": fields.String(required=True, description="Email")
})

reset_password_model = api.model("Reset Password", {
  "new_password": fields.String(required=True, description="New Password")
})

profile_model = api.model("Profile", {
  "name": fields.String(required=True, description="Name"),
  "username": fields.String(required=True, description="Username"),
  "email": fields.String(required=True, description="Email")
})

data_model = api.model("Data", {
  "source": fields.String(required=True, description="Source"),
  "sentiment": fields.String(required=True, description="Sentiment"),
  "text": fields.String(required=True, description="Text"),
})