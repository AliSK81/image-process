class FaceBoxPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __dict__(self):
        return {
            "x": self.x,
            "y": self.y
        }
