from typing import List

def chunking_text(text : str, chunk_size : int = 20, overlap: int = 2):
    chunks = []

    start  = 0 

    while start < len(text):
        end = min(start + chunk_size , len(text))

        chunk = text[start:end]

        chunks.append(chunk)

        start =end - overlap
        
        
    return chunks