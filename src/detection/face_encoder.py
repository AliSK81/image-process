import threading

import face_recognition


class FaceEncoder:
    def __init__(self):
        self.lock = threading.Lock()

    def encode_image(self, image):
        with self.lock:
            return face_recognition.face_encodings(image)
