from typing import List

def chunking_text(text : str, chunk_size : int = 200, overlap: int = 35):
    chunks = []

    start  = 0 

    while start < len(text):
        end = min(start + chunk_size , len(text))

        chunk = text[start:end]

        chunks.append(chunk)

        start =end - overlap
        
        
    return chunks