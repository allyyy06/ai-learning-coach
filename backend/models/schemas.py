from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    goal: str
    level: str
    daily_time: int
    learning_style: str
    xp: int = 0
    streak_days: int = 0
    last_active_date: Optional[datetime] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LearningPlanBase(BaseModel):
    user_id: int
    plan_data: Dict[str, Any]
    status: str = "active"

class LearningPlanResponse(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    plan_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = "active"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    error: Optional[bool] = False
    message: Optional[str] = None

    class Config:
        from_attributes = True

class DailyProgressCreate(BaseModel):
    user_id: int
    content: str

class DailyProgressResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    content: str
    performance_score: Optional[float]
    feedback: Optional[str]
    raw_analysis: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class PerformanceReportResponse(BaseModel):
    id: int
    user_id: int
    report_type: str
    summary: str
    metrics: Dict[str, Any]
    suggestions: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressSubmissionResponse(BaseModel):
    progress: DailyProgressResponse
    coach_feedback: Dict[str, Any]

class QuizResponse(BaseModel):
    id: int
    user_id: int
    daily_progress_id: int
    questions: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class QuizSubmit(BaseModel):
    user_id: int
    quiz_id: int
    answers: List[int]

class QuizAttemptResponse(BaseModel):
    score: float
    correct_count: int
    total_questions: int
    attempt_id: int
