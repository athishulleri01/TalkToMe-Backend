from sqlalchemy.orm import Session
from . import models

# Get a single post by post_id
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()

# Get all posts
def get_posts(db: Session):
    return db.query(models.Post).all()

# Create a new post
def create_post(db: Session, post: models.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Update an existing post
def update_post(db: Session, post_id: int, updated_post: models.PostCreate):
    db_post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if db_post:
        for attr, value in updated_post.dict(exclude_unset=True).items():
            setattr(db_post, attr, value)
        db.commit()
        db.refresh(db_post)
    return db_post

# Delete a post by post_id
def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
