from sqlalchemy.orm import Session
from ..database.models import UserProfile
from ..models.schemas import UserProfileCreate

def create_profile(db: Session, profile: UserProfileCreate):
    db_profile = UserProfile(
        full_name=profile.full_name,
        age=profile.age,
        gender=profile.gender,
        goal=profile.goal,
        level=profile.level,
        daily_time=profile.daily_time,
        learning_style=profile.learning_style
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.id == user_id).first()
