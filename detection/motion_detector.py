import cv2


class MotionDetector:

    def __init__(self, threshold=5000):
        self.previous_gray = None
        self.threshold = threshold

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (21, 21),
            0
        )

        if self.previous_gray is None:
            self.previous_gray = gray
            return False, 0

        difference = cv2.absdiff(
            self.previous_gray,
            gray
        )

        _, threshold_image = cv2.threshold(
            difference,
            25,
            255,
            cv2.THRESH_BINARY
        )

        threshold_image = cv2.dilate(
            threshold_image,
            None,
            iterations=2
        )

        motion_pixels = cv2.countNonZero(
            threshold_image
        )

        self.previous_gray = gray

        return (
            motion_pixels > self.threshold,
            motion_pixels
        )