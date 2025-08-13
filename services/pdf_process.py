# pdf process service
from typing import List
from pypdf import PdfReader
import os
from services.chunking import chunk_text

class pdfprocess:
    def extract(pdf_path: str) -> List[str]:
        reader = PdfReader(pdf_path)
        chunks = []

        for page in reader.pages:  
            text = page.extract_text()  
            if text:  
                page_chunks = chunk_text(text)
                chunks.extend(page_chunks)
        return chunks  


    def upload(upload_file, save_path: str) -> str:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            f.write(upload_file.file.read())

        return save_path