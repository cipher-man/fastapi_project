from .. import schemas,utils, models
from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"] # This tags will list all user path togthere in the web documentation
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": f"User with id {user_id} not found."})
    return user