import io
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_bytes = pdf_file.read()
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        pass

    if not text.strip():
        images = convert_from_bytes(pdf_bytes)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.lower()
