from typing import Optional

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


def extract_text_from_docx(file) -> str:
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text_from_upload(upload) -> str:
    """
    Given a Streamlit UploadedFile, detect type and extract text.
    """
    if upload is None:
        return ""

    suffix = upload.name.lower().split(".")[-1]
    if suffix == "pdf":
        return extract_text_from_pdf(upload)
    if suffix in ("docx", "doc"):
        return extract_text_from_docx(upload)

    # Fallback to plain text
    try:
        return upload.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


