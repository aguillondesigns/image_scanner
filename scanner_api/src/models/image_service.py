from db import get_db
from .image import Image


class ImageService:
    def get_images(ids: list = None):
        images: list = []
        db = get_db()
        cursor = db.cursor()
        query = "select * from `images` where "
        if ids is not None:
            query += "`id` in (" + ",".join(ids) + ")"
        else:
            query += "1"
        cursor.execute(query)
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

    def get_image_objects():
        images: list = []
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select `id`,`objects` from `images` where 1")
        results = cursor.fetchall()

        if len(results) > 0:
            for row in results:
                id = row[0]
                objects: str = "" if row[1] == None else row[1].split(",")
                img = Image(id, None, objects, None, False)
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
        # our return data
        filtered = []

        if filter is not None:
            # keep our payload minimal when searching
            images = ImageService.get_image_objects()
            filters = ImageService.parse_filter(filter)
            filtered_ids = []
            for f in filters:
                for image in images:
                    if f in image.objects:
                        filtered_ids.append(str(image.id))
            # now that we have the ids we want, grab those
            images = ImageService.get_images(filtered_ids)
        else:
            # no filter, get them all
            images = ImageService.get_images()

        # serialize our data
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
