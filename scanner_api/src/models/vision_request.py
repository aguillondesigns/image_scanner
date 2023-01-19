import requests
import os
from .vision_response import VisionResponse

VISION_API = os.environ.get("VISION_API")
VISION_APIKEY = os.environ.get("VISION_APIKEY")


class VisionRequest:
    request = None
    url = None

    # We only need to send the image to get our data back
    def __init__(this, content: str):
        this.url = f"{VISION_API}{VISION_APIKEY}"
        request = {
            "requests": [
                {
                    "features": [
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 10},
                        {"type": "IMAGE_PROPERTIES", "maxResults": 20},
                        {"type": "LABEL_DETECTION", "maxResults": 10},
                    ],
                    "image": {"content": content},
                }
            ]
        }

        this.request = request

    def post(this):
        response = requests.post(this.url, json=this.request)
        return VisionResponse(response)
