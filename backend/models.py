from sqlalchemy import Column, Integer, String, JSON
from database import Base


class UserProfileDB(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    education = Column(String, nullable=False)
    skills = Column(JSON, nullable=False)
    interests = Column(JSON, nullable=False)
    career_goal = Column(String, nullable=False)