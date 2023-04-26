from adapters.image_adapter import ImageAdapter
from detection.face_detector import FaceDetector


class FaceDetectionService:
    def __init__(self, face_detector: FaceDetector,
                 image_adapter: ImageAdapter):
        self.face_detector = face_detector
        self.image_adapter = image_adapter

    def detect_faces(self, img_bytes):
        image = self.image_adapter.bytes_to_numpy(img_bytes=img_bytes)
        face_locations = self.face_detector.detect_faces(image)
        return face_locations
