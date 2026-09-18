from pathlib import Path
from datetime import datetime

import cv2


def save_image(
    image,
    directory,
    prefix="image"
):

    directory = Path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    path = directory / (
        f"{prefix}_{timestamp}.jpg"
    )

    cv2.imwrite(
        str(path),
        image
    )

    return str(path)