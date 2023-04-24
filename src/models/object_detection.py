from models.face_box import FaceBox


class ObjectDetection:
    def __init__(self, face_box: FaceBox, confidence: float):
        self.face_box = face_box
        self.confidence = confidence

    def __dict__(self):
        return {
            "face_box": self.face_box.__dict__(),
            "confidence": self.confidence
        }
