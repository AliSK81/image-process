from typing import List

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from models.entities.image import Image


class Database:
    def __init__(self, host: str = 'localhost', port: int = 27017, max_pool_size: int = 50):
        self.__client = MongoClient(host=host, port=port, maxPoolSize=max_pool_size)

    def get_connection(self):
        try:
            connection = self.__client.get_database('face_rec')
            return connection
        except ConnectionFailure as e:
            print("Error connecting to database: ", e)

    def save_images(self, images: List[Image]):
        connection = self.get_connection()
        face_metadata_collection = connection.get_collection('images')
        face_metadata_collection.insert_many([image.__dict__ for image in images])

    def find_all_images(self) -> List[Image]:
        connection = self.get_connection()
        images_collection = connection.get_collection('images')

        documents = images_collection.find({})
        images = []
        for document in documents:
            image = Image(image_id=document['image_id'],
                          encodings=document['encodings'],
                          metadata=document['metadata'])
            images.append(image)
        return images

    def delete_images(self, image_ids: List[str]) -> int:
        connection = self.get_connection()
        images_collection = connection.get_collection('images')

        result = images_collection.delete_many({'image_id': {'$in': image_ids}})
        num_deleted = result.deleted_count

        return num_deleted
