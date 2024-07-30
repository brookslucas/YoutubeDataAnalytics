from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class VideoProfile(Base):
    __tablename__ = 'profile_table'
    id = Column(Integer, primary_key = True)
    video_id = Column(String, index = True)
    title = Column(String)
    channel_title = Column(String)
    publish_time = Column(DateTime)
    views = Column(Integer)
    likes = Column(Integer)
    dislikes = Column(Integer)
    like_ratio = Column(Float)
    category_name = Column(String)
    days_till_viral = Column(Integer)

# Setup the database connection and sessionmaker
engine = create_engine('sqlite:///youtube_video_profiles.db')
Base.metadata.create_all(engine)
