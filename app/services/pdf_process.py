from typing import List
from pdfminer.high_level import extract_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
import io

class PDFProcess:
    def extract_text(self, pdf_bytes: bytes) -> str:
        reader =  extract_text(io.BytesIO(pdf_bytes))
        return reader
    def split_text(self, text: str, chunk_size: int = 250, chunk_overlap: int = 27) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return splitter.split_text(text)
