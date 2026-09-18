from pathlib import Path

import cv2
import numpy as np


class FaceRecognizer:

    def __init__(self, known_faces_directory):

        self.directory = Path(
            known_faces_directory
        )

        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.known_faces = {}

        self.load_known_faces()

    def load_known_faces(self):

        self.known_faces.clear()

        supported_extensions = [
            ".jpg",
            ".jpeg",
            ".png"
        ]

        for file in self.directory.iterdir():

            if file.suffix.lower() not in supported_extensions:
                continue

            image = cv2.imread(
                str(file),
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                print(
                    f"Could not read image: {file}"
                )
                continue

            image = cv2.resize(
                image,
                (100, 100)
            )

            # Make sure stored image is uint8
            image = np.asarray(
                image,
                dtype=np.uint8
            )

            name = file.stem

            self.known_faces[name] = image

            print(
                f"Loaded registered face: {name}"
            )

    def recognize(self, face_image):

        if face_image is None:
            return "Unknown", 0.0

        if not self.known_faces:
            return "Unknown", 0.0

        # Convert live face to grayscale if needed
        if len(face_image.shape) == 3:

            face = cv2.cvtColor(
                face_image,
                cv2.COLOR_BGR2GRAY
            )

        else:

            face = face_image.copy()

        # Resize to exactly the same dimensions
        face = cv2.resize(
            face,
            (100, 100)
        )

        # Force same data type
        face = np.asarray(
            face,
            dtype=np.uint8
        )

        best_name = "Unknown"
        best_score = float("inf")

        for name, known_face in self.known_faces.items():

            # Force known image to uint8 too
            known_face = np.asarray(
                known_face,
                dtype=np.uint8
            )

            # Make absolutely sure dimensions match
            if face.shape != known_face.shape:

                known_face = cv2.resize(
                    known_face,
                    (100, 100)
                )

            difference = cv2.absdiff(
                face,
                known_face
            )

            score = float(
                np.mean(difference)
            )

            if score < best_score:

                best_score = score
                best_name = name

        # Prototype recognition threshold
        if best_score < 55:

            confidence = max(
                0.0,
                100.0 - best_score
            )

            return best_name, confidence

        return "Unknown", 0.0

    def reload(self):

        self.load_known_faces()