from fastapi import FastAPI
from sqlalchemy import create_engine
from models import VideoProfile  # Ensure you have this model defined as shown previously
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from schemas import VideoProfileSchema  # Importing the Pydantic schema
from typing import List  # Importing the List type for response_model

app = FastAPI()

# Database connection setup
DATABASE_URL = "sqlite:///./youtube_video_profiles.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/videos/{video_id}", response_model=VideoProfileSchema)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(VideoProfile).filter(VideoProfile.id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@app.get("/videos/", response_model=List[VideoProfileSchema])
def get_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = db.query(VideoProfile).offset(skip).limit(limit).all()
    return videos
