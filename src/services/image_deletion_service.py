from database.database import Database


class ImageDeletionService:
    def __init__(self, database: Database):
        self.database = database

    def delete_images(self, image_ids):
        self.database.delete_images(image_ids)
