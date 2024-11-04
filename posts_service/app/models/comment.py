from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    user_id: int
    post_id: int
    comment_text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    comment_id: int
    created_at: datetime

    class Config:
        orm_mode = True
