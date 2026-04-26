from sqlalchemy.orm import Session
from ..database.models import Quiz, QuizAttempt, DailyProgress, UserProfile
from ..agents.evaluator_agent import EvaluatorAgent
from .plan_service import update_plan_dynamically
import json

evaluator = EvaluatorAgent()

def create_quiz_for_progress(db: Session, progress_id: int):
    progress = db.query(DailyProgress).filter(DailyProgress.id == progress_id).first()
    if not progress:
        return None
    
    user = db.query(UserProfile).filter(UserProfile.id == progress.user_id).first()
    if not user:
        return None

    # Check if quiz already exists for this progress
    existing_quiz = db.query(Quiz).filter(Quiz.daily_progress_id == progress_id).first()
    if existing_quiz:
        return existing_quiz

    # Find the topic for this progress in the plan
    from .plan_service import get_latest_plan
    active_plan = get_latest_plan(db, user.id)
    topic = "Bilinmiyor"
    
    if active_plan:
        # Determine current day by counting progress entries before this one
        progress_count = db.query(DailyProgress).filter(
            DailyProgress.user_id == user.id,
            DailyProgress.date <= progress.date
        ).count()
        
        # Extract topic from plan data
        try:
            plan_data = active_plan.plan_data
            days = []
            for week in plan_data.get("weeks", []):
                days.extend(week.get("days", []))
            
            if progress_count <= len(days):
                topic = days[progress_count - 1].get("topic", "Genel")
            else:
                topic = days[-1].get("topic", "Genel")
        except:
            topic = "Genel Öğrenme"

    quiz_dict = evaluator.generate_quiz(goal=user.goal, content=progress.content, topic=topic)
    
    if quiz_dict.get("error"):
        return quiz_dict

    db_quiz = Quiz(
        user_id=user.id,
        daily_progress_id=progress_id,
        questions=quiz_dict.get("questions", [])
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def submit_quiz_attempt(db: Session, user_id: int, quiz_id: int, answers: list):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None

    correct_count = 0
    questions = quiz.questions
    
    for i, ans in enumerate(answers):
        if i < len(questions):
            if int(ans) == int(questions[i]["correct_index"]):
                correct_count += 1
    
    score = (correct_count / len(questions)) * 100 if questions else 0
    
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        answers=answers,
        score=score
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    # Adaptive Logic: Trigger plan update if score is very low or perfect
    if score < 40:
        summary = f"Son bilgi yarışması puanı: {score:.0f}/100. Kullanıcı konuyu kavramakta zorlanıyor. Lütfen planı basitleştirin ve temel konulara odaklanın."
        update_plan_dynamically(db, user_id, summary)
    elif score == 100:
        # Maybe check if they also have high progress score
        summary = f"Son bilgi yarışması puanı: 100/100. Kullanıcı konuyu mükemmel kavradı. Lütfen planı biraz daha zorlaştırın veya yeni bir konuya geçin."
        # We don't always want to change plan on every 100, but it's a good trigger
        update_plan_dynamically(db, user_id, summary)

    return {
        "score": score,
        "correct_count": correct_count,
        "total_questions": len(questions),
        "attempt_id": attempt.id
    }

def get_user_quizzes(db: Session, user_id: int):
    return db.query(Quiz).filter(Quiz.user_id == user_id).order_by(Quiz.created_at.desc()).all()
