from flask import Flask, jsonify, request

import di
from common.logger import Logger
from services.face_detection_service import FaceDetectionService
from services.face_enrolling_service import FaceEnrollingService
from services.face_searching_service import FaceSearchingService
from services.image_deletion_service import ImageDeletionService

app = Flask(__name__)


@app.route("/", methods=["GET"])
def ping():
    di.injector.get(Logger).log('service is up')
    return jsonify({"message": "Service is up!"})


@app.route("/api/v1/auth/", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    return jsonify({"token": "temp-token"})


@app.route("/api/v1/face/enroll/", methods=["POST"])
def face_enroll():
    image_bytes = request.files["image"].read()
    image_id = request.form["image_id"]
    metadata = request.form["metadata"]

    di.injector.get(FaceEnrollingService).enroll_images(
        images=[image_bytes],
        image_ids=[image_id],
        metadata=metadata
    )

    return jsonify({
        "image_id": image_id,
        "status": "200",
        "msg": "OK"
    })


@app.route("/api/v1/face/bulkEnroll/", methods=["POST"])
def face_bulk_enroll():
    di.injector.get(Logger).log('bulk enroll started')

    metadata = request.form["metadata"]
    image_ids = request.form.getlist("image_ids")
    images = request.files.getlist("images")
    images_bytes = [image.read() for image in images]

    di.injector.get(Logger).log('bulk data ready')

    di.injector.get(FaceEnrollingService).enroll_images(
        images=images_bytes,
        image_ids=image_ids,
        metadata=metadata
    )

    di.injector.get(Logger).log('bulk enroll done')

    response_data = [{
        "image_id": image_id,
        "status": "200",
        "msg": "OK"
    } for image_id in image_ids]

    return jsonify(response_data)


@app.route("/api/v1/face/detect/", methods=["POST"])
def face_detect():
    image_bytes = request.files["image"].read()

    face_boxes = di.injector.get(FaceDetectionService).detect_faces(image_bytes)

    response_data = []
    for face_box in face_boxes:
        a, b, c, d = face_box
        left_down = [b, a]
        right_up = [d, c]
        height = left_down[0] - right_up[0]
        left_up = [left_down[0] - height, left_down[1]]
        right_down = [right_up[0] + height, right_up[1]]
        response_data.append({
            "faceBox": [left_up, right_down],
            "confidence": 1
        })

    return jsonify(response_data)


@app.route("/api/v1/face/bulkDelete/", methods=["POST"])
def face_bulk_delete():
    metadata = request.form["metadata"]
    image_ids = request.form.getlist("image_ids")
    di.injector.get(ImageDeletionService).delete_images(image_ids)
    return jsonify({"detail": "OK"})


@app.route("/api/v1/search/", methods=["POST"])
def search():
    image_bytes = request.files["image"].read()
    threshold = float(request.form["threshold"])
    page = int(request.form["page"])
    page_size = int(request.form["page_size"])
    metadata = request.form["metadata"]

    search_result = di.injector.get(FaceSearchingService).search_image(
        img_bytes=image_bytes,
        threshold=threshold
    )

    return jsonify(search_result)


if __name__ == '__main__':
    app.run(debug=True)
