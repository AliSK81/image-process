import face_recognition


class FaceDetector:
    def detect_faces(self, image):
        return face_recognition.face_locations(image)

    def compute_landmarks(self, image, face_locations):
        return [face_recognition.face_landmarks(image, [location])[0] for location in face_locations]
