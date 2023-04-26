from matplotlib import pyplot as plt, patches

from adapters.image_adapter import ImageAdapter
from database.database import Database
from detection.face_detector import FaceDetector
from detection.face_encoder import FaceEncoder
from detection.face_searcher import FaceSearcher
from models.entities.face_encoding import FaceEncoding
from models.requests.image_search_request import ImageSearchRequest
from services.face_enrolling_service import FaceEnrollingService
from services.face_searching_service import FaceSearchingService

if __name__ == "__main__":
    img_adapter = ImageAdapter()
    face_encoder = FaceEncoder()
    face_detector = FaceDetector()
    face_searcher = FaceSearcher()
    db = Database.get_instance()
    #
    with open('known_faces.png', 'rb') as f:
        known_faces_bytes = f.read()

    known_faces = img_adapter.bytes_to_numpy(img_bytes=known_faces_bytes, grayscale=False)
    encodings = face_encoder.encode_image(image=known_faces)
    known_faces_locations = face_detector.detect_faces(image=known_faces)

    # Save the encodings to the database
    faces_encodings = [FaceEncoding(face_id=i, encoding=encoding) for i, encoding in enumerate(encodings)]
    db.save_face_encodings(faces_encodings)

    # draw green rectangle around detected faces
    fig, ax = plt.subplots()
    ax.imshow(known_faces)
    for (top, right, bottom, left) in known_faces_locations:
        rect = patches.Rectangle((left, top), right - left, bottom - top, linewidth=2, edgecolor='g', facecolor='none')
        ax.add_patch(rect)

    with open('unknown_faces.png', 'rb') as f:
        unknown_faces_bytes = f.read()

    searcher = FaceSearcher(face_encodings=db.get_all_face_encodings())
    unknown_faces = img_adapter.bytes_to_numpy(img_bytes=unknown_faces_bytes, grayscale=False)
    found_faces = searcher.search_image(image=unknown_faces)
    # draw red rectangle around found faces
    for face_id, confidence in found_faces:
        top, right, bottom, left = known_faces_locations[face_id]
        rect = patches.Rectangle((left, top), right - left, bottom - top, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        print(f'face_id: {face_id}, confidence: {confidence}')

    plt.show()

    face_detection_service = FaceEnrollingService(face_encoder=face_encoder, database=db)
    # face_detection_service.enroll_images(images=[known_faces])
    #
    # face_search_service = FaceSearchingService(face_searcher=face_searcher, image_adapter=img_adapter, database=db)
    # search_result = face_search_service.search_image(request=ImageSearchRequest(file_content=unknown_faces_bytes))
    # print(search_result)
