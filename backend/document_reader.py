
from pathlib import Path
from io import BytesIO

import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_document(file_path: str) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    print("Reading document:", file_path)

    # JPG and PNG images
    if extension in [".jpg", ".jpeg", ".png"]:
        with Image.open(path) as image:
            return pytesseract.image_to_string(image).strip()

    # PDF documents
    if extension == ".pdf":
        extracted_pages = []

        with fitz.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                # Try extracting selectable text first.
                text = page.get_text().strip()

                # Scanned PDF pages may need OCR.
                if not text:
                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2),
                        alpha=False,
                    )

                    image = Image.open(
                        BytesIO(pix.tobytes("png"))
                    )

                    text = pytesseract.image_to_string(image).strip()

                extracted_pages.append(
                    f"Page {page_number}:\n{text}"
                )

        return "\n".join(extracted_pages).strip()

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Use JPG, JPEG, PNG, or PDF."
    )
