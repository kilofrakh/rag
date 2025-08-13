# schema
from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    top_k: int

class SearchResult(BaseModel):
    results: List[str]