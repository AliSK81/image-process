import os

from injector import Injector, Module, provider, singleton

from adapters.image_adapter import ImageAdapter
from common.logger import Logger
from database.database import Database
from detection.face_detector import FaceDetector
from detection.face_encoder import FaceEncoder
from detection.face_searcher import FaceSearcher
from services.face_detection_service import FaceDetectionService
from services.face_enrolling_service import FaceEnrollingService
from services.face_searching_service import FaceSearchingService
from services.image_deletion_service import ImageDeletionService


class AppModule(Module):
    @singleton
    @provider
    def provide_face_encoder(self) -> FaceEncoder:
        return FaceEncoder()

    @provider
    def provide_image_adapter(self) -> ImageAdapter:
        return ImageAdapter()

    @singleton
    @provider
    def provide_database(self) -> Database:
        return Database(host=os.environ.get('MONGO_DB_HOST', 'localhost'),
                        port=int(os.environ.get('MONGO_DB_PORT', '27017')))

    @provider
    def provide_face_encoding_service(
            self,
            face_encoder: FaceEncoder,
            image_adapter: ImageAdapter,
            database: Database
    ) -> FaceEnrollingService:
        return FaceEnrollingService(
            face_encoder=face_encoder,
            image_adapter=image_adapter,
            database=database
        )

    @provider
    def provide_face_detection_service(
            self,
            face_detector: FaceDetector,
            image_adapter: ImageAdapter
    ) -> FaceDetectionService:
        return FaceDetectionService(
            face_detector=face_detector,
            image_adapter=image_adapter
        )

    @provider
    def provide_face_searching_service(
            self,
            face_searcher: FaceSearcher,
            image_adapter: ImageAdapter,
            face_encoder: FaceEncoder,
            database: Database
    ) -> FaceSearchingService:
        return FaceSearchingService(
            face_searcher=face_searcher,
            image_adapter=image_adapter,
            face_encoder=face_encoder,
            database=database
        )

    @provider
    def provide_image_deletion_service(
            self,
            database: Database
    ) -> ImageDeletionService:
        return ImageDeletionService(
            database=database
        )

    @singleton
    @provider
    def provider_logger(self) -> Logger:
        return Logger(filename='app.log')


injector = Injector(AppModule())
