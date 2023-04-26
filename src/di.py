import injector

from adapters.face_detector_adapter import FaceDetectorAdapter
from adapters.image_adapter import ImageAdapter
from database.database import Database
from detection.face_encoder import FaceEncoder
from services.face_detection_service import FaceDetectionService
from services.face_enrolling_service import FaceEnrollingService
from services.face_searching_service import FaceSearchingService
from services.image_deletion_service import ImageDeletionService


class AppModule(injector.Module):
    def configure(self, binder):
        binder.bind(FaceEncoder)
        binder.bind(FaceDetectorAdapter)
        binder.bind(ImageAdapter)
        binder.bind(Database, to=Database.get_instance(), scope=injector.singleton)

        binder.bind(FaceEnrollingService)
        binder.bind(FaceDetectionService)
        binder.bind(FaceSearchingService)
        binder.bind(ImageDeletionService)


injector_instance = injector.Injector([AppModule])


def get_face_encoder() -> FaceEncoder:
    return injector_instance.get(FaceEncoder)


def get_face_detector_adapter() -> FaceDetectorAdapter:
    return injector_instance.get(FaceDetectorAdapter)


def get_image_adapter() -> ImageAdapter:
    return injector_instance.get(ImageAdapter)


def get_database() -> Database:
    return injector_instance.get(Database)


def get_face_enrolling_service() -> FaceEnrollingService:
    return injector_instance.get(FaceEnrollingService)


def get_face_detection_service() -> FaceDetectionService:
    return injector_instance.get(FaceDetectionService)


def get_face_searching_service() -> FaceSearchingService:
    return injector_instance.get(FaceSearchingService)


def get_image_deletion_service() -> ImageDeletionService:
    return injector_instance.get(ImageDeletionService)
