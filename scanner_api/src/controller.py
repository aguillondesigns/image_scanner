from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from models.image import Image
from models.image_service import ImageService
from models.request_handler import RequestHandler

app = Flask(__name__)
CORS(app, expose_headers=["X-Source-Host"])

# GET with/without args
@app.route("/images", methods=["GET"])
def get_images():
    filter = request.args.get("objects")
    filtered_images = ImageService.filter_images(filter)
    if len(filtered_images) == 0:
        return make_response(jsonify({"message": "no images found"}), 200)
    return make_response(jsonify(filtered_images), 200)


# GET by id
@app.route("/images/<int:id>/", methods=["GET"])
def get_image_by_id(id):
    image = ImageService.get_image(id)
    if image is not None:
        return make_response(jsonify([image.serialize()]), 200)
    else:
        return make_response(jsonify({"error": "image not found"}), 404)


# POST data
@app.route("/images", methods=["POST"])
def post_image():
    # Grab our json
    json_request = request.get_json(silent=True)
    if json_request is not None:
        # Ensures all request params are present(even if null)
        valid_request = RequestHandler.validate_request(json_request)
        # Now that our json is valid, check it
        response = RequestHandler.handle_request(valid_request)
        return response

    # json data not found,
    response = make_response(
        jsonify({"error": "invalid or missing json request data"}), 400
    )
    return response
