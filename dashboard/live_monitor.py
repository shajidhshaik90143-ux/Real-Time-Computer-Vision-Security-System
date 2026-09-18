import cv2
import time
from datetime import datetime

import streamlit as st

from camera.camera_manager import CameraManager
from detection.motion_detector import MotionDetector
from detection.person_detector import PersonDetector
from detection.face_detector import FaceDetector
from recognition.face_encoder import FaceEncoder
from recognition.face_recognizer import FaceRecognizer
from alerts.alert_manager import AlertManager


def run_live_monitor(
    camera_index,
    model_name,
    confidence,
    database,
    evidence_dir,
    known_faces_dir
):

    camera = CameraManager(camera_index)

    if not camera.start():

        st.error(
            "❌ Camera could not be opened."
        )

        st.info(
            "Check that your webcam is connected "
            "and not being used by another application."
        )

        return

    motion_detector = MotionDetector()

    person_detector = PersonDetector(
        model_name,
        confidence
    )

    face_detector = FaceDetector()

    encoder = FaceEncoder()

    recognizer = FaceRecognizer(
        known_faces_dir
    )

    alert_manager = AlertManager()

    frame_placeholder = st.empty()

    info_placeholder = st.empty()

    stop_button = st.button(
        "🛑 Stop Camera"
    )

    last_motion_event = 0
    last_person_event = 0
    last_face_event = 0

    while camera.is_opened() and not stop_button:

        success, frame = camera.read()

        if not success:
            st.error(
                "Unable to read camera frame."
            )
            break

        motion, motion_pixels = (
            motion_detector.detect(frame)
        )

        persons = person_detector.detect(
            frame
        )

        faces = face_detector.detect(
            frame
        )

        frame = person_detector.draw(
            frame,
            persons
        )

        frame = face_detector.draw(
            frame,
            faces
        )

        current_time = time.time()

        # Motion event
        if motion and (
            current_time - last_motion_event > 5
        ):

            evidence_path = save_evidence(
                frame,
                evidence_dir,
                "motion"
            )

            database.add_event(
                "Motion Detected",
                f"Motion pixels: {motion_pixels}",
                "MEDIUM",
                evidence_path
            )

            alert_manager.create_alert(
                "Motion",
                "Motion detected by camera."
            )

            last_motion_event = current_time

        # Person event
        if len(persons) > 0 and (
            current_time - last_person_event > 5
        ):

            evidence_path = save_evidence(
                frame,
                evidence_dir,
                "person"
            )

            database.add_event(
                "Person Detected",
                f"{len(persons)} person(s) detected.",
                "INFO",
                evidence_path
            )

            last_person_event = current_time

        # Face event
        if len(faces) > 0:

            for x, y, w, h in faces:

                face_crop = frame[
                    y:y+h,
                    x:x+w
                ]

                encoded_face = encoder.extract_face(
                    face_crop
                )

                name, score = recognizer.recognize(
                    encoded_face
                )

                if name == "Unknown":

                    cv2.putText(
                        frame,
                        "UNKNOWN",
                        (x, y + h + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

                    if (
                        current_time - last_face_event
                        > 10
                    ):

                        evidence_path = save_evidence(
                            frame,
                            evidence_dir,
                            "unknown_face"
                        )

                        database.add_event(
                            "Unknown Face",
                            "An unregistered face was detected.",
                            "HIGH",
                            evidence_path
                        )

                        alert_manager.create_alert(
                            "Unknown Face",
                            "Unknown face detected."
                        )

                        last_face_event = (
                            current_time
                        )

                else:

                    cv2.putText(
                        frame,
                        f"{name} {score:.1f}",
                        (x, y + h + 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 0),
                        2
                    )

        # Convert BGR -> RGB
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            frame_rgb,
            channels="RGB",
            use_container_width=True
        )

        info_placeholder.markdown(
            f"""
            **Camera:** 🟢 Active  
            **Persons:** `{len(persons)}`  
            **Faces:** `{len(faces)}`  
            **Motion Pixels:** `{motion_pixels}`  
            **Last Update:** `{datetime.now().strftime("%H:%M:%S")}`
            """
        )

        time.sleep(0.03)

    camera.stop()

    st.warning(
        "Camera monitoring stopped."
    )


def save_evidence(
    frame,
    evidence_dir,
    event_name
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    filename = (
        f"{event_name}_{timestamp}.jpg"
    )

    path = evidence_dir / filename

    cv2.imwrite(
        str(path),
        frame
    )

    return str(path)