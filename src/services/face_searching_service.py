from adapters.image_adapter import ImageAdapter
from database.database import Database
from detection.face_encoder import FaceEncoder
from detection.face_searcher import FaceSearcher


class FaceSearchingService:
    def __init__(self, face_searcher: FaceSearcher, image_adapter: ImageAdapter, face_encoder: FaceEncoder,
                 database: Database):
        self.face_searcher = face_searcher
        self.image_adapter = image_adapter
        self.face_encoder = face_encoder
        self.database = database

    def search_image(self, img_bytes, threshold):
        image = self.image_adapter.bytes_to_numpy(img_bytes=img_bytes, grayscale=False)
        query_encoding = self.face_encoder.encode_image(image)[0]
        images = self.database.find_all_images()
        matched_faces = self.face_searcher.search(query_encoding=query_encoding, images=images, threshold=threshold)
        return matched_faces
