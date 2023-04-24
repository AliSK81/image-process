import face_recognition


class FaceEncoder:
    def encode_image(self, image):
        return face_recognition.face_encodings(image)
