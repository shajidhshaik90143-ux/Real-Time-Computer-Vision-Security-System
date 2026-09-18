import cv2


class FaceDetector:

    def __init__(self):

        cascade_path = cv2.data.haarcascades + (
            "haarcascade_frontalface_default.xml"
        )

        self.detector = cv2.CascadeClassifier(
            cascade_path
        )

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )

        return faces

    def draw(self, frame, faces):

        for index, (x, y, w, h) in enumerate(faces):

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Face {index + 1}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        return frame