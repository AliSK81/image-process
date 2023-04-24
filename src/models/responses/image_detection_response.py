from models.object_detection import ObjectDetection


class ImageDetectionResponse:
    def __init__(self, detected_objects: [ObjectDetection]):
        self.detected_objects = detected_objects

    def __dict__(self):
        detected_objects_list = []
        for obj in self.detected_objects:
            detected_objects_list.append(obj.__dict__())
        return {"detected_objects": detected_objects_list}
