import cv2
from ultralytics import YOLO


class PersonDetector:

    def __init__(
        self,
        model_name="yolo11n.pt",
        confidence=0.45
    ):
        self.model = YOLO(model_name)
        self.confidence = confidence

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        for box in result.boxes:

            class_id = int(
                box.cls[0].item()
            )

            confidence = float(
                box.conf[0].item()
            )

            # COCO class 0 = person
            if class_id != 0:
                continue

            coordinates = box.xyxy[0].tolist()

            x1, y1, x2, y2 = map(
                int,
                coordinates
            )

            detections.append({
                "class": "person",
                "confidence": confidence,
                "box": (x1, y1, x2, y2)
            })

        return detections

    def draw(self, frame, detections):

        for detection in detections:

            x1, y1, x2, y2 = detection["box"]

            confidence = detection["confidence"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"Person {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return frame