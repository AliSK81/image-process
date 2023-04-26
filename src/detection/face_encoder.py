import concurrent.futures
import face_recognition

class FaceEncoder:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def encode_image(self, image):
        return self.executor.submit(face_recognition.face_encodings, image)
