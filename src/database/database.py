from threading import Lock
from typing import List

import numpy as np
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from models.entities.face_encoding import FaceEncoding
from models.entities.face_metadata import FaceMetadata
from models.entities.image import Image


class Database:
    __instance = None
    __client = None
    __lock = Lock()

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            Database.__client = MongoClient(host='localhost', port=27017, maxPoolSize=50)

    def get_connection(self):
        try:
            connection = Database.__client.get_database('face_rec')
            return connection
        except ConnectionFailure as e:
            print("Error connecting to database: ", e)

    def save_face_encodings(self, face_encodings: List[FaceEncoding]):
        connection = self.get_connection()
        face_encodings_collection = connection.get_collection('face_encodings')

        for face_encoding in face_encodings:
            document = {
                'face_id': face_encoding.face_id,
                'encoding': face_encoding.encoding.tolist()
            }
            face_encodings_collection.insert_one(document)

    def save_face_metadata(self, face_metadata: List[FaceMetadata]):
        connection = self.get_connection()
        face_metadata_collection = connection.get_collection('face_metadata')

        for metadata in face_metadata:
            document = {
                'face_id': metadata.face_id,
                'metadata': metadata.metadata
            }
            face_metadata_collection.insert_one(document)

    def get_face_encoding(self, face_id: str) -> FaceEncoding:
        connection = self.get_connection()
        face_encodings_collection = connection.get_collection('face_encodings')

        document = face_encodings_collection.find_one({'face_id': face_id})
        if document is not None:
            encoding = np.array(document['encoding'])
            return FaceEncoding(face_id=face_id, encoding=encoding)
        else:
            raise Exception(f'face_id {face_id} does not exist.')

    def get_face_metadata(self, face_id: str) -> FaceMetadata:
        connection = self.get_connection()
        face_metadata_collection = connection.get_collection('face_metadata')

        document = face_metadata_collection.find_one({'face_id': face_id})
        if document is not None:
            metadata = document['metadata']
            return FaceMetadata(face_id=face_id, metadata=metadata)
        else:
            raise Exception(f'face_id {face_id} does not exist.')

    def get_all_face_encodings(self) -> List[FaceEncoding]:
        connection = self.get_connection()
        face_encodings_collection = connection.get_collection('face_encodings')

        documents = face_encodings_collection.find({})
        face_encodings = []
        for document in documents:
            face_id = document['face_id']
            encoding = np.array(document['encoding'])
            face_encoding = FaceEncoding(face_id=face_id, encoding=encoding)
            face_encodings.append(face_encoding)
        return face_encodings

    def save_images(self, images):
        connection = self.get_connection()
        face_metadata_collection = connection.get_collection('images')
        for image in images:
            face_metadata_collection.insert_one(image)

    def find_all_images(self):
        connection = self.get_connection()
        images_collection = connection.get_collection('images')

        documents = images_collection.find({})
        images = []
        for document in documents:
            image = Image(image_id=document['image_id'],
                          encodings=[np.array(encoding) for encoding in document['encodings']],
                          metadata=document['metadata'])
            images.append(image)
        return images

    def delete_images(self, image_ids):
        connection = self.get_connection()
        images_collection = connection.get_collection('images')

        result = images_collection.delete_many({'image_id': {'$in': image_ids}})
        num_deleted = result.deleted_count

        return num_deleted
