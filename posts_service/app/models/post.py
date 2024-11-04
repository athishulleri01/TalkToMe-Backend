from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    user_id: int
    caption: str
    image_url: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
