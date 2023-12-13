# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, current_user

# local imports
from .. import api, db, authorizations
from ..models import Data
from ..api_models import data_response_model, data_model
from ..utils import generate_response


data_ns = Namespace("Data", path="/data", description="Operations about Data", authorizations=authorizations)

@data_ns.route("")
@data_ns.doc(responses={200: "OK", 201: "Created"}, security="jsonWebToken")
class DataList(Resource):
  method_decorators = [jwt_required()]
  def get(self):
    """Get a list of all datas."""
    datas = Data.query.filter_by(user_id=current_user.id).all()
    return generate_response(200, "Request processed successful", api.marshal(datas, data_response_model)), 200

  @data_ns.expect(data_model)
  def post(self):
    """Add a new data."""
    api.payload["user"] = current_user

    new_data = Data(**api.payload)
    db.session.add(new_data)
    db.session.commit()
    return generate_response(201, "Data created successful", api.marshal(new_data, data_response_model)), 201

@data_ns.route("/<id>")
@data_ns.doc(responses={204: "No Content", 403: "Forbidden", 404: "Not Found"}, params={"id": "Data ID"}, security="jsonWebToken")
class DataResource(Resource):
  method_decorators = [jwt_required()]
  def get(self, id):
    """Get data by ID."""
    data = Data.query.get(id)
    if not data:
      return generate_response(404, "Data not found"), 404
    # check if the current user is the owner of the data
    if data.user_id != current_user.id:
      return generate_response(403, "You do not have permission to access this data"), 403
    return generate_response(200, "Request processed successful", api.marshal(data, data_response_model)), 200

  @data_ns.expect(data_model)
  def put(self, id):
    """Update datas by ID."""
    data = Data.query.get(id)
    if not data:
      return generate_response(404, "Data not found"), 404

    if "source" in api.payload:
      data.source = api.payload["source"]
    if "sentiment" in api.payload:
      data.sentiment = api.payload["sentiment"]
    if "text" in api.payload:
      data.text = api.payload["text"]

    db.session.commit()
    return generate_response(200, "Data updated successful", api.marshal(data, data_response_model)), 200

  def delete(self, id):
    """Delete datas by ID."""
    data = Data.query.get(id)
    if not data:
      return generate_response(404, "Data not found"), 404
    # check if the current user is the owner of the data
    if data.user_id != current_user.id:
      return generate_response(403, "You do not have permission to access this data"), 403

    db.session.delete(data)
    db.session.commit()
    return generate_response(204, "Data deleted successful", api.marshal(data, data_response_model)), 204