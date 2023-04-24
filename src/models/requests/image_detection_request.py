class ImageDetectionRequest:
    def __init__(self, file_name: str, file_content: [bytes]):
        self.file_name = file_name
        self.file_content = file_content

    @staticmethod
    def from_dict(data: dict):
        return ImageDetectionRequest(data['file_name'], data['file_content'])
