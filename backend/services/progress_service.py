from sqlalchemy.orm import Session
from ..database.models import DailyProgress, UserProfile
from ..agents.evaluator_agent import EvaluatorAgent
from ..agents.coach_agent import CoachAgent
from .plan_service import update_plan_dynamically

evaluator = EvaluatorAgent()
coach = CoachAgent()

from datetime import datetime

def submit_progress(db: Session, user_id: int, content: str):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        return None
    
    # 1. Evaluate Progress
    evaluation = evaluator.evaluate_progress(goal=user.goal, progress_report=content)
    if evaluation.get("error"):
        return {"error": True, "message": evaluation.get("message")}
    
    # 2. Get Coach Feedback
    user_profile_dict = {
        "goal": user.goal,
        "level": user.level,
        "style": user.learning_style
    }
    feedback_dict = coach.give_feedback(evaluation_results=evaluation, user_profile=user_profile_dict)
    if feedback_dict.get("error"):
        return {"error": True, "message": feedback_dict.get("message")}
    
    # --- Gamification Logic ---
    today = datetime.utcnow().date()
    user.xp = (user.xp or 0) + 50
    
    if user.last_active_date:
        last_active = user.last_active_date.date()
        diff = (today - last_active).days
        if diff == 1:
            user.streak_days = (user.streak_days or 0) + 1
        elif diff > 1:
            user.streak_days = 1
    else:
        user.streak_days = 1
        
    user.last_active_date = datetime.utcnow()
    # --- End Gamification Logic ---

    # 3. Save to DB
    db_progress = DailyProgress(
        user_id=user_id,
        content=content,
        performance_score=evaluation.get("performance_score"),
        feedback=feedback_dict.get("coach_feedback"),
        raw_analysis=evaluation
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    
    # 4. Adaptive Engine: If score is very low or very high, consider updating plan
    # For now, let's trigger update if score < 40 or score > 95
    score = evaluation.get("performance_score", 50)
    if score < 40 or score > 95:
        summary = f"Son performans puanı: {score}. Analiz: {evaluation.get('analysis')}"
        update_plan_dynamically(db, user_id, summary)
        
    return {
        "progress": db_progress,
        "coach_feedback": feedback_dict
    }

def get_progress_history(db: Session, user_id: int):
    return db.query(DailyProgress).filter(DailyProgress.user_id == user_id).order_by(DailyProgress.date.desc()).all()
