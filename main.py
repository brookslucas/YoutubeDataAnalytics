from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Depends
from sqlalchemy import create_engine
from models import VideoProfile  # Ensure you have this model defined as shown previously
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import sessionmaker, Session
from schemas import VideoProfileSchema  # Importing the Pydantic schema
from typing import List  # Importing the List type for response_model
from aws_utils import upload_to_s3
import shutil
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


app = FastAPI(docs_url=None, redoc_url="/docs")

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
def get_video(video_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single video by its ID.

    - **video_id**: unique identifier of the video
    """
    video = db.query(VideoProfile).filter(VideoProfile.video_id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@app.get("/videos/", response_model=List[VideoProfileSchema])
def get_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = db.query(VideoProfile).offset(skip).limit(limit).all()
    return videos

@app.post("/videos/", response_model=VideoProfileSchema)
def add_video(video: VideoProfileSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_video = VideoProfile(**video.dict())
    db.add(db_video)
    db.commit()
    background_tasks.add_task(analyze_video_engagement, db_video.id, db)
    return db_video

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    location = f"temp/{file.filename}"
    with open(location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Now upload to S3
    result = upload_to_s3(location, "ydapibucket")
    if result:
        return {"message": "File uploaded successfully"}
    else:
        return {"message": "File upload failed"}


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css"
    )
