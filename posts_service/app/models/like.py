from pydantic import BaseModel
from datetime import datetime

class LikeBase(BaseModel):
    user_id: int
    post_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    like_id: int
    created_at: datetime

    class Config:
        orm_mode = True
