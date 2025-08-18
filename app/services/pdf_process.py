from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import io

def split_text(text: str, chunk_size: int = 250, chunk_overlap: int = 27) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


class PDFProcess:
    def extract(self, pdf_file) -> List[str]:
        reader = PdfReader(pdf_file)
        full_text = "".join(page.extract_text() or "" for page in reader.pages)
        return split_text(full_text)



    async def upload(self, upload_file) -> io.BytesIO:
        file_bytes = await upload_file.read()
        
        return io.BytesIO(file_bytes)
