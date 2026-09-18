import cv2
import numpy as np


class FaceEncoder:

    def __init__(self):

        cascade_path = (
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        self.face_detector = (
            cv2.CascadeClassifier(cascade_path)
        )

    def extract_face(self, image):

        if image is None:
            return None

        if image.size == 0:
            return None

        # Convert to grayscale
        if len(image.shape) == 3:

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

        else:

            gray = image.copy()

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:

            # If the supplied image is already a face crop,
            # use the complete crop.
            face = gray

        else:

            x, y, w, h = faces[0]

            face = gray[
                y:y + h,
                x:x + w
            ]

        if face.size == 0:
            return None

        face = cv2.resize(
            face,
            (100, 100)
        )

        # Always return uint8
        face = np.asarray(
            face,
            dtype=np.uint8
        )

        return face