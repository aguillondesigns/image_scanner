from db import get_db


class VisionResponse:
    objects = []
    names = []
    response_text = None

    def __init__(this, response):
        this.objects = []
        this.names = []
        this.response_text = response.text

        # Grab our json object
        json = response.json()
        responses = json["responses"]
        for response in responses:
            # Houses the different lables the item can go by
            label_anns = response["labelAnnotations"]
            for ann in label_anns:
                score = ann["score"]
                if score > 0.75:
                    this.objects.append(ann["description"].lower())

            # Houses what the object is most likely called
            object_anns = response["localizedObjectAnnotations"]
            for ann in object_anns:
                name = ann["name"]
                this.names.append(name)

        print(this.objects, this.names)

    # save our vision response
    def log(this, image_id: int):
        db = get_db()
        cursor = db.cursor()

        query = "insert into `response_log` (`imageid`,`data`) values (%s, %s)"
        params = (image_id, this.response_text)
        cursor.execute(query, params)
        db.commit()
