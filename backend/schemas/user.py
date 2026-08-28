from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str
    education: str
    skills: list[str]
    interests: list[str]
    career_goal: str