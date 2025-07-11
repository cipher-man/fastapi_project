from .. import schemas,utils, models
from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from . import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0, search:Optional[str] = ""):
    # cursor.execute("SELECT * FROM post")
    # all_posts = cursor.fetchall()
    print(skip)
    print(limit)
    all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).all()

    if all_posts is None:
        return JSONResponse(status_code=404, content={"message": "No posts found."})
    return results

@router.get("/latest")
async def get_latest_post(db: Session = Depends(get_db)):
    #cursor.execute("SELECT * FROM post ORDER BY ID DESC LIMIT 1")
    #latest_post = cursor.fetchone()
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if latest_post is None:
        return JSONResponse(status_code=404, content={"message": "No posts found."})
    return latest_post

@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_posts(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # METHOD 1: USING SQL CURSOR:
    #cursor.execute('''SELECT * FROM post WHERE "ID" = %s''', (str(post_id)))
    # post_id = cursor.fetchone()
    spec_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    post_ot = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.id == post_id).group_by(models.Post.id).first()
    if spec_post is None:
        return JSONResponse(status_code=404, content={"message": f"Post with id {post_id} not found."})
    return post_ot


@router.post("/", response_model=schemas.postResponse, status_code=status.HTTP_201_CREATED, )
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #METHOD 1: USING SQL CURSOR:
    # USING SQL STATMENTS
    #cursor.execute(f"INSERT INTO post (title,content, published) VALUES ('{post.title}', '{post.content}', {post.published})") --> This is vulnerable to SQL injection DONT DO THIS
    # cursor.execute('INSERT INTO post ("Title", "Content", "Published") VALUES (%s, %s, %s) RETURNING *',(post.Title, post.Content, post.Published))
    # new_post = cursor.fetchone()
    # conn.commit() 

    #END OF METHOD 1

    


    # METHOD 2: USING SQLALCHEMY ORM:
    # This is the recommended way to do it
    #new_post = models.Post(title=post.Title, content=post.Content, published=post.Published) --> WE CAN DO THIS BUT THEIR BETTER WAY
    
    print(current_user.email)
    current_user_id = current_user.id  
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{post_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM post WHERE "ID" = %s RETURNING *''', (str(post_id)))
    # del_post = cursor.fetchone()
    # conn.commit()
    

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        return JSONResponse(status_code=404, content={"message": f"Post with id {post_id} not found."})
    if post.owner_id != current_user.id:
        return JSONResponse(status_code=403, content={"message": "You are not authorized to delete this post."})
    db.delete(post)
    db.commit()
    return {"message": f"Post with id {post_id} has been deleted."}

@router.put("/{post_id}")
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE post SET "Title" = %s, "Content" = %s, "Published" = %s WHERE "ID" = %s RETURNING *''', 
    #                (post.Title, post.Content, post.Published, str(post_id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if updated_post is None:
        return JSONResponse(status_code=404, content={"message": f"Post with id {post_id} not found."})
    if updated_post.owner_id != current_user.id:
        return JSONResponse(status_code=403, content={"message": "You are not authorized to update this post."})

    for key, value in post.dict().items():
        setattr(updated_post, key, value)

    db.commit()
    db.refresh(updated_post)
    return updated_post
