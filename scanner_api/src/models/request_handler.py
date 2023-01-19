from flask import jsonify, make_response
import requests
import base64
from .image import Image
from .image_service import ImageService
from .vision_request import VisionRequest


class RequestHandler:
    # Returns a valid structure for processing
    def validate_request(json):
        title = "" if "title" not in json else json["title"]
        detection = True if "use_detection" not in json else json["use_detection"]
        image = None if "image" not in json else json["image"]
        url = None if "url" not in json else json["url"]
        return {"title": title, "use_detection": detection, "image": image, "url": url}

    # Performs most of the data validation
    def handle_request(json: dict):
        # if we have no image or image url, we are done here
        if json["image"] is None and json["url"] is None:
            return RequestHandler.make_error(json, "[image] or [url] must be supplied")

        # image not supplied, fetch from the url
        if json["image"] is None:
            image = RequestHandler.get_image(json["url"])
            # image headers are not jpeg/png
            if image is None:
                return RequestHandler.make_error(
                    json, "[url] supplied may not be an image url"
                )
            json["image"] = image
        else:
            valid_image = RequestHandler.is_base64(json["image"])
            # base64 issue
            if valid_image == False:
                return RequestHandler.make_error(json, "[image] supplied is invalid")

        # our image at this point is base64 encoded
        json["image"] = str(json["image"])

        # create our table entry
        create_data = Image.create(json["image"], json["title"], json["use_detection"])
        if isinstance(create_data, int) == False:
            return RequestHandler.make_error(json, create_data)

        image = ImageService.get_image(create_data)
        save_image = False

        # Use our google image detection
        if json["use_detection"]:
            vision_request = VisionRequest(image.image)
            vision_response = vision_request.post()

            # logging for testing
            vision_response.log(create_data)

            image.objects = vision_response.objects
            if image.title is None or image.title == "":
                image.title = f"{vision_response.names[0].lower()} {image.id}"
                json["title"] = image.title
            save_image = True
        # Verify we have some kind of title
        else:
            if image.title is None:
                image.title = f"image {image.id}"
                save_image = True

        if save_image:
            save = image.save()
            if save is not None:
                RequestHandler.make_error(image.serialize(), save)

        response = {
            "id": create_data,
            "message": "resource created",
            "status": "success",
            "request": json,
        }

        return make_response(jsonify(response), 200)

    # download and convert an image to base64 encoded data
    def get_image(url: str):
        formats = ("image/jpeg", "image/png")
        req = requests.get(url)
        headers = req.headers
        if headers["Content-Type"] in formats:
            encoded = base64.b64encode(requests.get(url).content)
            return encoded.decode("ascii")
        return None

    # Handle our error/request concatenation
    def make_error(json, msg):
        response = {"request": json, "message": msg, "status": "error"}
        return make_response(jsonify(response), 400)

    # quick check to see if decoding/re-encoding yeilds the same result
    def is_base64(contents):
        try:
            decoded = base64.b64decode(contents)  # byte array
            encoded = base64.b64encode(decoded)
            is_base64 = len(contents) == len(encoded)
            return is_base64
        except:
            return False
