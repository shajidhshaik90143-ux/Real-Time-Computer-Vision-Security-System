import cv2
import time


class CameraManager:

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = None

    def start(self):

        print(
            f"Opening camera {self.camera_index}..."
        )

        # Use OpenCV's default Windows backend
        self.camera = cv2.VideoCapture(
            self.camera_index
        )

        if not self.camera.isOpened():

            print(
                "❌ Camera could not be opened."
            )

            self.stop()

            return False

        # Use a modest resolution for better compatibility
        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        # Give the webcam time to initialize
        time.sleep(1)

        # Read several frames
        valid_frame = None

        for _ in range(20):

            success, frame = self.camera.read()

            if success and frame is not None:

                valid_frame = frame

        if valid_frame is None:

            print(
                "❌ Camera opened but no frame was received."
            )

            self.stop()

            return False

        brightness = float(
            valid_frame.mean()
        )

        print(
            f"Camera brightness: {brightness:.2f}"
        )

        if brightness < 1:

            print(
                "⚠️ Camera is returning an almost black frame."
            )

        else:

            print(
                "✅ Camera is returning an image."
            )

        return True

    def read(self):

        if self.camera is None:
            return False, None

        if not self.camera.isOpened():
            return False, None

        success, frame = self.camera.read()

        if not success:
            return False, None

        if frame is None:
            return False, None

        return True, frame

    def stop(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None

    def is_opened(self):

        return (
            self.camera is not None
            and self.camera.isOpened()
        )