from typing import List
from pypdf import PdfReader
from services.chunking import split_text
import os

class PDFProcess:
    def extract(pdf_path:str ) -> List[str]:
        reader = PdfReader(pdf_path)
        chunks = split_text(page.extract_text() for page in reader.pages)
        return chunks
        
        
    def upload(upload_file, save_path : str) -> str:

            os.makedirs(os.path.dirname(save_path), exist_ok= True)

            with open(save_path, 'wb')as f:
                f.write(upload_file.file.read())

            return save_path