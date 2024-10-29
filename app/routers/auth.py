from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.schema import UserIn, UserOut
from app.auth.utils import hash_password, authenticate_user
from app.auth.jwt_manager import create_access_token
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserIn, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user_in.username, hashed_password=hash_password(user_in.password))
    db.add(new_user)
    db.commit()
    return UserOut(username=new_user.username)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
