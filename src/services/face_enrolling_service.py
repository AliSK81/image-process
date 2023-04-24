from adapters.image_adapter import ImageAdapter
from database.database import Database
from detection.face_encoder import FaceEncoder


class FaceEnrollingService:
    def __init__(self, face_encoder: FaceEncoder, image_adapter: ImageAdapter, database: Database):
        self.face_encoder = face_encoder
        self.database = database
        self.image_adapter = image_adapter

    def enroll_images(self, images, image_ids, metadata):
        if len(images) != len(image_ids):
            raise ValueError('Number of images is not equal to image_ids count.')

        encoded_images = []
        for image, image_id in zip(images, image_ids):
            image_array = self.image_adapter.bytes_to_numpy(image)
            encodings = self.face_encoder.encode_image(image_array)
            encoded_image = {
                'image_id': image_id,
                'encodings': [encoding.tolist() for encoding in encodings],
                'metadata': metadata
            }
            encoded_images.append(encoded_image)

        self.database.save_images(encoded_images)
