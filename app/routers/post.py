from .. import models, oath2, utils
from ..schemas import PostCreate, PostResponse, PostOut
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: int = Depends(oath2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ''
                    ):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user = Depends(oath2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    utils.check_queried_post(post_query, current_user, id)

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    utils.check_queried_post(post_query, current_user, id)

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()