from pdfminer.high_level import extract_text
from typing import List
import io

def split_text(text: str, chunk_size: int = 250, chunk_overlap: int = 27) -> List[str]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

class PDFProcess:
    def extract(self, pdf_file) -> List[str]:
        text = extract_text(pdf_file)
        return split_text(text or "")

    async def upload(self, upload_file) -> io.BytesIO:
        file_bytes = await upload_file.read()
        
        return io.BytesIO(file_bytes)
