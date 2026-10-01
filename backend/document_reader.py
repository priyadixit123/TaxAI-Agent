from pathlib import Path

import pytesseract
from PIL import Image


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_document(file_path: str) -> str:

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension not in [".jpg", ".jpeg", ".png"]:
        raise ValueError(
            f"Currently OCR supports JPG, JPEG and PNG. "
            f"Received: {extension}"
        )

    print("OCR reading:", file_path)

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text.strip()