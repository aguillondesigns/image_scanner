from db import get_db
import mysql.connector


class Image(object):
    id: int = None
    title: str = None
    objects: list = []
    image: str = None
    detection: bool = True

    def __init__(this, id, title="", objects="", image="", detection=False):
        this.id = id
        this.title = title
        this.objects = objects
        this.image = image
        this.detection = detection

    def serialize(this):
        return {
            "id": this.id,
            "title": this.title,
            "objects": this.objects,
            "use_detection": this.detection,
            "image": this.image,
        }

    def create(body: str, title: str = "", detection: bool = True):
        # Grab our db connector, get our cursor
        db = get_db()
        cursor = db.cursor()

        # setup our query and params
        query = "insert into `images` (`title`, `image`, `use_detection`) values (%s, %s, %s)"
        params = (title, body, detection)
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.errors.IntegrityError:
            return f"title of '{title}' is already in use"

        return cursor.lastrowid

    def save(this):
        # Grab db cursor
        db = get_db()
        cursor = db.cursor()

        # only the title and the objects will change
        query = "update `images` set `title` = %s, `objects` = %s where `id` = %s"
        params = (this.title, ",".join(this.objects), this.id)

        try:
            cursor.execute(query, params)
            db.commit()
        except:
            return f"error update image id {this.id}"

        return None
