from models.face_box_point import FaceBoxPoint


class FaceBox:
    def __init__(self, left_up: FaceBoxPoint, right_down: FaceBoxPoint):
        self.left_up = left_up
        self.right_down = right_down

    def __dict__(self):
        return {
            "left_up": self.left_up.__dict__(),
            "right_down": self.right_down.__dict__()
        }
