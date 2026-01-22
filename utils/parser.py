
from io import BytesIO
from typing import Optional
import docx2txt
from PyPDF2 import PdfReader

def extract_text(file_bytes: bytes, filename: str) -> Optional[str]:
    """Extracts raw text from PDF or DOCX bytes."""
    name = filename.lower()
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(BytesIO(file_bytes))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)
        elif name.endswith(".docx"):
            bio = BytesIO(file_bytes)
            text = docx2txt.process(bio)
            return text or ""
        else:
            return None
    except Exception as e:
        return None
