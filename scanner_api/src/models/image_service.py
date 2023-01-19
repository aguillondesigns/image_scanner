from db import get_db
from .image import Image


class ImageService:
    def get_images():
        images: list = []
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from `images` where 1")
        results = cursor.fetchall()
        if len(results) > 0:
            for row in results:
                id = row[0]
                title = row[1]
                objects: str = "" if row[2] == None else row[2].split(",")
                body: str = row[3]
                detection: bool = row[4]
                img = Image(id, title, objects, body, detection)
                images.append(img)
        return images

    def get_image(id: int):
        db = get_db()
        cursor = db.cursor()
        query = "select * from `images` where `id` = %s"
        params = (id,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result is not None:
            title = result[1]
            detected_objects = "" if result[2] == None else result[2].split(",")
            body = result[3]
            detection = result[4]
            return Image(id, title, detected_objects, body, detection)

        return None

    def filter_images(filter=None):
        images = ImageService.get_images()
        filtered = []
        if filter is not None:
            filters = ImageService.parse_filter(filter)
            for f in filters:
                for image in images:
                    if f in image.objects:
                        filtered.append(image.serialize())
        else:
            for image in images:
                filtered.append(image.serialize())

        return filtered

    def parse_filter(filter: str):
        filters = []
        if "," in filter:
            pieces = filter.split(",")
            for piece in pieces:
                filters.append(piece.strip())
        else:
            filters.append(filter.strip())

        return filters
