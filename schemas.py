# schemas.py
from pydantic import BaseModel
from typing import Optional

class IssueBase(BaseModel):
    key: str
    time_estimate: Optional[int]
    timespent: Optional[int]
    status: Optional[str]
    priority: Optional[str]

    class Config:
        orm_mode = True
