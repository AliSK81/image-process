import multiprocessing as mp

import face_recognition


class FaceEncoder:
    def __init__(self, num_processes=1):
        self.num_processes = num_processes

    def encode_image(self, image):
        with mp.Pool(self.num_processes) as pool:
            results = pool.map(self._encode_image_worker, [image])
        return results[0]

    def _encode_image_worker(self, image):
        return face_recognition.face_encodings(image)
