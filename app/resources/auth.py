# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, jwt_required, current_user

# local imports
from .. import api, db, bcrypt, authorizations
from ..models import User
from ..api_models import register_response_model, login_response_model, forgot_password_response_model, register_model, login_model, change_password_model, forgot_password_model, reset_password_model, profile_model
from ..utils import generate_response


auth_ns = Namespace("Auth", path="/auth", description="Operations about Auth", authorizations=authorizations)

@auth_ns.route("/register")
@api.doc(responses={201: "Created", 400: "Bad Request"})
class Register(Resource):
  @auth_ns.expect(register_model)
  def post(self):
    """Create an account."""
    # check if the username is already registered
    existing_user_username = User.query.filter_by(username=api.payload["username"]).first()
    if existing_user_username:
      return generate_response(400, "Username is already registered"), 400

    # check if the email is already registered
    existing_user_email = User.query.filter_by(email=api.payload["email"]).first()
    if existing_user_email:
      return generate_response(400, "Email is already registered"), 400

    # hash the password
    api.payload["password"] = bcrypt.generate_password_hash(api.payload["password"]).decode("utf-8")

    new_user = User(**api.payload)
    db.session.add(new_user)
    db.session.commit()
    return generate_response(201, "Account created successful", api.marshal(new_user, register_response_model)), 201

@auth_ns.route("/login")
@api.doc(responses={200: "OK", 401: "Unauthorized"})
class Login(Resource):
  @auth_ns.expect(login_model)
  def post(self):
    """Log in to your account."""
    user = User.query.filter_by(username=api.payload["username"]).first()
    if not user:
      return generate_response(401, "Username is not registered"), 401
    if not bcrypt.check_password_hash(user.password, api.payload["password"]):
      return generate_response(401, "Incorrect password"), 401

    access_token = create_access_token(user)
    user.token = "Bearer " + access_token

    db.session.commit()
    return generate_response(200, "Login successful", api.marshal(user, login_response_model)), 200

@auth_ns.route("/change-password")
@auth_ns.doc(responses={200: "OK", 401: "Unauthorized"}, security="jsonWebToken")
class ChangePassword(Resource):
  method_decorators = [jwt_required()]
  @auth_ns.expect(change_password_model)
  def put(self):
    """Change your account password."""
    user = User.query.get(current_user.id)
    # verify the current password
    if not bcrypt.check_password_hash(user.password, api.payload["current_password"]):
      return generate_response(401, "Incorrect current password"), 401

    # hash and update the new password
    user.password = bcrypt.generate_password_hash(api.payload["new_password"]).decode("utf-8")

    db.session.commit()
    return generate_response(200, "Password changed successful", api.marshal(user, register_response_model)), 200

@auth_ns.route("/forgot-password")
@auth_ns.doc(responses={200: "OK", 401: "Unauthorized"})
class ForgotPassword(Resource):
  @auth_ns.expect(forgot_password_model)
  def post(self):
    """Initiate the password reset process."""
    user = User.query.filter_by(email=api.payload["email"]).first()
    if not user:
      return generate_response(401, "Email is not registered"), 401

    token = user.get_reset_token()
    user.reset_token = token

    db.session.commit()
    return generate_response(200, "Password reset initiated successful", api.marshal(user, forgot_password_response_model)), 200

@auth_ns.route("/reset-password/<token>")
@auth_ns.doc(responses={200: "OK", 404: "Not Found"}, params={"token": "Reset password token"})
class ResetPassword(Resource):
  @auth_ns.expect(reset_password_model)
  def post(self, token):
    """Reset the password using the provided token."""
    user = User.verify_reset_token(token)
    if not user:
      return generate_response(404, "Invalid or expired token"), 404

    # hash and update the user password
    user.password = bcrypt.generate_password_hash(api.payload["new_password"]).decode("utf-8")

    db.session.commit()
    return generate_response(200, "Password reset successful", api.marshal(user, register_response_model)), 200

@auth_ns.route("/profile")
@auth_ns.doc(responses={200: "OK", 403: "Forbidden", 404: "Not Found"}, security="jsonWebToken")
class Profile(Resource):
  method_decorators = [jwt_required()]
  def get(self):
    """Get profile account details."""
    user = User.query.get(current_user.id)
    if not user:
      return generate_response(404, "Account not found"), 404
    # check if the current user is the owner of the profile
    if user.id != current_user.id:
      return generate_response(403, "You do not have permission to access this profile"), 403
    return generate_response(200, "Request processed successful", api.marshal(user, register_response_model)), 200

  @auth_ns.expect(profile_model)
  def put(self):
    """Update profile account."""
    user = User.query.get(current_user.id)
    if not user:
      return generate_response(404, "Account not found"), 404

    if "name" in api.payload:
      user.name = api.payload["name"]

    if "username" in api.payload:
      # check if the new username is not already registered
      existing_user_username = User.query.filter(User.id != current_user.id, User.username == api.payload["username"]).first()
      if existing_user_username:
        return generate_response(400, "Username is already registered"), 400
      user.username = api.payload["username"]

    if "email" in api.payload:
      # check if the new email is not already registered
      existing_user_email = User.query.filter(User.id != current_user.id, User.email == api.payload["email"]).first()
      if existing_user_email:
        return generate_response(400, "Email is already registered"), 400
      user.email = api.payload["email"]

    db.session.commit()
    return generate_response(200, "Profile updated successful", api.marshal(user, register_response_model)), 200