from sqlalchemy.orm import Session
from ..database.models import LearningPlan, UserProfile
from ..agents.planner_agent import PlannerAgent
import json

planner = PlannerAgent()

def generate_and_save_plan(db: Session, user_id: int):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        return None
    
    plan_dict = planner.generate_plan(
        goal=user.goal,
        level=user.level,
        daily_time=user.daily_time,
        learning_style=user.learning_style
    )
    
    if plan_dict.get("error"):
        # Don't save to DB if there's an error
        return plan_dict
    
    db_plan = LearningPlan(
        user_id=user_id,
        plan_data=plan_dict,
        status="active"
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_latest_plan(db: Session, user_id: int):
    return db.query(LearningPlan).filter(
        LearningPlan.user_id == user_id, 
        LearningPlan.status == "active"
    ).order_by(LearningPlan.created_at.desc()).first()

def update_plan_dynamically(db: Session, user_id: int, performance_summary: str):
    current_plan = get_latest_plan(db, user_id)
    if not current_plan:
        return None
    
    updated_plan_dict = planner.update_plan(
        current_plan=current_plan.plan_data,
        performance_summary=performance_summary
    )
    
    # Archive current plan
    current_plan.status = "archived"
    
    # Create new plan
    new_plan = LearningPlan(
        user_id=user_id,
        plan_data=updated_plan_dict,
        status="active"
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan
