from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
EVIDENCE_DIR = BASE_DIR / "evidence"
LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"
KNOWN_FACES_DIR = BASE_DIR / "known_faces"

for directory in [
    DATA_DIR,
    EVIDENCE_DIR,
    LOG_DIR,
    MODEL_DIR,
    KNOWN_FACES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "security.db"

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))

YOLO_MODEL = os.getenv("YOLO_MODEL", "yolo11n.pt")

CONFIDENCE_THRESHOLD = float(
    os.getenv("CONFIDENCE_THRESHOLD", "0.45")
)

MOTION_THRESHOLD = int(
    os.getenv("MOTION_THRESHOLD", "5000")
)

FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (50, 50)

EVENT_COOLDOWN_SECONDS = 5