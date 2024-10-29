from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import User
from app.auth.jwt_manager import decode_access_token
from langfuse import Langfuse
from app.auth.utils import oauth2_scheme


# Definição da exceção para credenciais inválidas
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_langfuse():
    return Langfuse()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

def get_trace_handler(langfuse: Langfuse = Depends(get_langfuse), user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    trace = langfuse.trace(user_id=user.username)
    return trace.get_langchain_handler()
