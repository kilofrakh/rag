from typing import List
from pypdf import PdfReader
from chunking import split_text

class PDFProcess:
    def extract(pdf_path:str ) -> List[str]:
        reader = PdfReader(pdf_path)
        
        return [page.extract_text() for page in reader.pages]
    
