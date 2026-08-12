from app.services.pdf_loader import extract_text
from app.services.chunker import chunk_text

extracted_text = extract_text("app/scripts/Final_Research_Paper.pdf")
chunked_text = chunk_text(extracted_text)

for text in chunked_text:
    print("===========" + text + "\n")