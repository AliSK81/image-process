from io import BytesIO

import face_recognition
import numpy as np


class ImageAdapter:
    def bytes_to_numpy(self, img_bytes: bytes, grayscale: bool = False) -> np.ndarray:
        return face_recognition.load_image_file(BytesIO(img_bytes))
        # img_pil = Image.open(BytesIO(img_bytes))
        #
        # if grayscale:
        #     img_pil = img_pil.convert('L')
        # img_np = np.array(img_pil)
        #
        # return img_np
