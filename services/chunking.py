# chunking services
from typing import List


def chunk_text(text: str, chunk_size: int = 50, overlap: int = 12) -> List[str]:
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap 
        
    return chunks
