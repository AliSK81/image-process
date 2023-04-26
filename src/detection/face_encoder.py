import multiprocessing
import face_recognition


class FaceEncoder:
    def __init__(self, num_processes=10):
        self.pool = multiprocessing.Pool(num_processes)

    def encode_image(self, image):
        result = self.pool.apply_async(face_recognition.face_encodings, (image,))
        return result.get()
