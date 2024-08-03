from io import BytesIO

import fitz


def extract_text_from_pdf(file: BytesIO) -> str:
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text
