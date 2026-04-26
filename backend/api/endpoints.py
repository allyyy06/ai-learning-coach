from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models import schemas
from ..services import profile_service, plan_service, progress_service, quiz_service, report_service

router = APIRouter()

@router.post("/create-profile", response_model=schemas.UserProfileResponse)
def create_profile(profile: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    return profile_service.create_profile(db, profile)

@router.get("/get-profile", response_model=schemas.UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = profile_service.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.post("/generate-plan", response_model=schemas.LearningPlanResponse)
def generate_plan(user_id: int, db: Session = Depends(get_db)):
    plan = plan_service.generate_and_save_plan(db, user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="User not found")
    return plan

@router.get("/get-plan", response_model=schemas.LearningPlanResponse)
def get_plan(user_id: int, db: Session = Depends(get_db)):
    plan = plan_service.get_latest_plan(db, user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.post("/submit-progress", response_model=schemas.ProgressSubmissionResponse)
def submit_progress(progress: schemas.DailyProgressCreate, db: Session = Depends(get_db)):
    result = progress_service.submit_progress(db, progress.user_id, progress.content)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result

class UpdatePlanRequest(BaseModel):
    user_id: int
    summary: str

@router.post("/update-plan", response_model=schemas.LearningPlanResponse)
def update_plan(request: UpdatePlanRequest, db: Session = Depends(get_db)):
    plan = plan_service.update_plan_dynamically(db, request.user_id, request.summary)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan could not be updated")
    return plan

@router.get("/performance-history")
def get_history(user_id: int, db: Session = Depends(get_db)):
    return progress_service.get_progress_history(db, user_id)

class QuestionRequest(BaseModel):
    user_id: int
    question: str

@router.post("/ask-question")
def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    user = profile_service.get_profile(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare context
    user_info = {
        "full_name": user.full_name,
        "goal": user.goal,
        "level": user.level
    }
    
    # Get context
    from ..services import plan_service, progress_service
    from ..agents.coach_agent import CoachAgent
    coach = CoachAgent()
    
    current_plan = plan_service.get_latest_plan(db, request.user_id)
    history = progress_service.get_progress_history(db, request.user_id)
    
    plan_str = str(current_plan.plan_data) if current_plan else "Henüz bir plan oluşturulmamış."
    recent_prog = history[0].content if history else "Henüz ilerleme kaydedilmemiş."
    
    # Use Coach Agent specialized answer_question method
    response = coach.answer_question(
        question=request.question,
        user_profile=user_info,
        current_plan=plan_str,
        recent_progress=recent_prog
    )
    return response

@router.post("/generate-quiz", response_model=schemas.QuizResponse)
def generate_quiz(progress_id: int, db: Session = Depends(get_db)):
    try:
        quiz = quiz_service.create_quiz_for_progress(db, progress_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="İlerleme kaydı bulunamadı.")
        if isinstance(quiz, dict) and quiz.get("error"):
            raise HTTPException(status_code=500, detail=quiz.get("message"))
        return quiz
    except Exception as e:
        print(f"ERROR: Quiz generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit-quiz", response_model=schemas.QuizAttemptResponse)
def submit_quiz(submission: schemas.QuizSubmit, db: Session = Depends(get_db)):
    result = quiz_service.submit_quiz_attempt(db, submission.user_id, submission.quiz_id, submission.answers)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return result

@router.post("/generate-weekly-report")
def generate_weekly_report(user_id: int, db: Session = Depends(get_db)):
    report = report_service.generate_weekly_report(db, user_id)
    if not report:
        raise HTTPException(status_code=404, detail="No progress found for last week")
    return report

@router.get("/reports")
def get_reports(user_id: int, db: Session = Depends(get_db)):
    return report_service.get_reports(db, user_id)
