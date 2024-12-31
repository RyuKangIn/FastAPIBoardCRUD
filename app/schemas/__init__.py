from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str]= None
    is_done: Optional[bool]=None

class TaskResponse(BaseModel):
    id:int
    title:str
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True
