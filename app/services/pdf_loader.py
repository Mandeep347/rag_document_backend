from pypdf import PdfReader

def extract_text(pdf_path: str) -> str:
    reader =  PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    return full_text