from typing import List

from models.face_box import FaceBox
from models.face_box_point import FaceBoxPoint


class FaceDetectorAdapter:
    def convert(self, face_locations: List[tuple]) -> List[FaceBox]:
        face_boxes = []
        for location in face_locations:
            face_box = FaceBox(
                left_up=FaceBoxPoint(x=location[3], y=location[0]),
                right_down=FaceBoxPoint(x=location[1], y=location[2])
            )

            face_boxes.append(face_box.__dict__())
        return face_boxes
