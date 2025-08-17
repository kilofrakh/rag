from pydantic import BaseModel
from typing import Optional

class PDFUpload(BaseModel):
    name: str
    description: Optional[str] = None