from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from schemas.user import UserProfile
from database import engine, Base, SessionLocal
from models import UserProfileDB

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AI Career Assistant API is running!"}


@app.post("/profile")
def create_profile(profile: UserProfile, db: Session = Depends(get_db)):
    db_profile = UserProfileDB(
        name=profile.name,
        education=profile.education,
        skills=profile.skills,
        interests=profile.interests,
        career_goal=profile.career_goal
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return {
        "message": "Profile saved successfully!",
        "id": db_profile.id,
        "profile": profile
    }

@app.get("/profiles")
def get_profiles(db: Session = Depends(get_db)):
    profiles = db.query(UserProfileDB).all()

    return {
        "profiles": profiles
    }

@app.get("/profile/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfileDB).filter(
        UserProfileDB.id == profile_id
    ).first()

    if not profile:
        return {"message": "Profile not found"}

    return {
        "id": profile.id,
        "name": profile.name,
        "education": profile.education,
        "skills": profile.skills,
        "interests": profile.interests,
        "career_goal": profile.career_goal
    }

@app.put("/profile/{profile_id}")
def update_profile(
    profile_id: int,
    profile: UserProfile,
    db: Session = Depends(get_db)
):
    db_profile = db.query(UserProfileDB).filter(
        UserProfileDB.id == profile_id
    ).first()

    if not db_profile:
        return {"message": "Profile not found"}

    db_profile.name = profile.name
    db_profile.education = profile.education
    db_profile.skills = profile.skills
    db_profile.interests = profile.interests
    db_profile.career_goal = profile.career_goal

    db.commit()
    db.refresh(db_profile)

    return {
        "message": "Profile updated successfully!",
        "id": db_profile.id,
        "profile": profile
    }

@app.delete("/profile/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfileDB).filter(
        UserProfileDB.id == profile_id
    ).first()

    if not db_profile:
        return {"message": "Profile not found"}

    db.delete(db_profile)
    db.commit()

    return {
        "message": "Profile deleted successfully!",
        "id": profile_id
    }