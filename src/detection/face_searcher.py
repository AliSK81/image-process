import uuid

import face_recognition


class FaceSearcher:

    def search(self, query_encoding, images, threshold: float = 0.6):
        matched_faces = []
        for img in images:
            distances = face_recognition.face_distance(img.encodings, query_encoding)
            matches = [
                {'image_id': img.image_id,
                 'face_id': str(uuid.uuid4()),
                 # 'metadata': json.loads(img.metadata),
                 'similarity': (1 - distance)}
                for distance in distances
                if distance <= 1 - threshold
            ]
            matched_faces.extend(matches)
        return matched_faces
