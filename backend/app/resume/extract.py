from io import BytesIO
from pathlib import Path


def extract_resume_text(filename: str, data: bytes) -> tuple[str, list[str]]:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(data)
    if suffix == ".docx":
        return _extract_docx(data)
    if suffix in {".txt", ".md", ".text", ""}:
        return _decode(data), []
    if suffix in {".png", ".jpg", ".jpeg"}:
        return _decode(data), ["OCR worker is not enabled; decoded embedded text only."]
    return _decode(data), [f"Unsupported extension {suffix}; decoded as text."]


def _extract_pdf(data: bytes) -> tuple[str, list[str]]:
    try:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if text.strip():
            return text, []
        return _decode(data), ["PDF contained no extractable text; OCR is required."]
    except Exception:
        return _decode(data), ["PDF parser failed; decoded bytes as fallback text."]


def _extract_docx(data: bytes) -> tuple[str, list[str]]:
    try:
        from docx import Document

        document = Document(BytesIO(data))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        if text.strip():
            return text, []
        return _decode(data), ["DOCX contained no paragraph text."]
    except Exception:
        return _decode(data), ["DOCX parser failed; decoded bytes as fallback text."]


def _decode(data: bytes) -> str:
    return data.decode("utf-8", errors="ignore")
