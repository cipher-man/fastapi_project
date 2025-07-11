from fastapi import APIRouter, Depends, HTTPException, status
from .. import database
from .. import schemas, utils, models
from . import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

#OAuth2PasswordRequestForm:
# {
#     "username": "email",
#     "password": "password"
# }

@router.post("/login",response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: database.Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}