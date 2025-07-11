from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware #Adding CORS middleware

app = FastAPI()
origins = ["https://www.google.com", "https://www.facebook.com"]  # Example origins, adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, you can specify a list of allowed methods
    allow_headers=["*"],  # Allows all headers, you can specify a list of allowed headers
)
models.Base.metadata.create_all(bind=engine)



app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}




