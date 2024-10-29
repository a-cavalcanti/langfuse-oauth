from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/chat")
