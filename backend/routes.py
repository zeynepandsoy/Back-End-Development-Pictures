from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is not None:
        return jsonify(picture), 200
    else:
        return jsonify(message="Picture not found"), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Extract picture data from the request body
    picture_data = request.get_json()

    # Check if a picture with the same ID already exists
    picture_id = picture_data.get('id')
    for picture in data:
        if picture['id'] == picture_id:
            return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    # If not, add the new picture data to the list
    data.append(picture_data)

    # Return the created picture
    return jsonify(picture_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    picture_data = request.get_json()

    # Find the picture based on the given id
    for picture in data:
        if picture['id'] == id:
            # Update the existing picture with the incoming request data
            picture.update(picture_data)
            return jsonify(picture), 200

    # If the picture does not exist, return a 404 status with a message
    return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture by ID in the data list
    for picture in data:
        if picture['id'] == id:
            # Delete the picture from the list
            data.remove(picture)
            return '', 204  # Return an empty body with HTTP 204 status (NO_CONTENT)

    # If the picture does not exist, return a 404 status with a message
    return jsonify({"message": "picture not found"}), 404

