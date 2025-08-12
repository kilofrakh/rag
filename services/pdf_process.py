from typing import List
from pypdf import PdfReader
import os

class pdfprocess:
    def extract(pdf_path:str ) -> list[str]:
        reader = PdfReader(pdf_path)
        
        return [page.extract_text() for page in reader.pages]
    

    def upload(upload_file, save_path : str) -> str:

        os.makedirs(os.path.dirname(save_path), exist_ok= True)

        with open(save_path, 'wb')as f:
            f.write(upload_file.file.read())

        return save_path
    
