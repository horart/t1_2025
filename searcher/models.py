from pydantic import BaseModel
from typing import Optional

class ChatPromptModel(BaseModel):
    body: str

class ChatResponseModel(BaseModel):
    response: str