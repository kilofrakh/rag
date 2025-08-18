from typing import List
from pypdf import PdfReader
from services.chunking import split_text
import io

class PDFProcess:
    def extract(self, pdf_file) -> List[str]:
        reader = PdfReader(pdf_file)
        
        # Join all pages into one string (skip None safely)
        full_text = "".join(page.extract_text() or "" for page in reader.pages)
        
        # Now split into chunks
        chunks = split_text(full_text)
        return chunks

    async def upload(self, upload_file) -> bytes:
        file_bytes = await upload_file.read()
        return io.BytesIO(file_bytes)  # return file-like object
