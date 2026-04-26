from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    goal = Column(String, nullable=False)
    level = Column(String, nullable=False)  # Beginner, Intermediate, Advanced
    daily_time = Column(Integer, nullable=False)  # In minutes
    learning_style = Column(String, nullable=False)  # Visual, Auditory, Reading, Kinesthetic
    created_at = Column(DateTime, default=datetime.utcnow)
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_active_date = Column(DateTime, nullable=True)
    
    plans = relationship("LearningPlan", back_populates="user")
    progress_entries = relationship("DailyProgress", back_populates="user")

class LearningPlan(Base):
    __tablename__ = "learning_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    plan_data = Column(JSON, nullable=False)  # Structured weekly/daily plan
    status = Column(String, default="active")  # active, completed, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserProfile", back_populates="plans")

class DailyProgress(Base):
    __tablename__ = "daily_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)  # User's report of what they did
    performance_score = Column(Float, nullable=True)  # AI calculated score
    feedback = Column(Text, nullable=True)
    raw_analysis = Column(JSON, nullable=True)
    
    user = relationship("UserProfile", back_populates="progress_entries")


class PerformanceReport(Base):
    __tablename__ = "performance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    report_type = Column(String, default="weekly")
    summary = Column(Text)
    metrics = Column(JSON)
    suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    daily_progress_id = Column(Integer, ForeignKey("daily_progress.id"))
    questions = Column(JSON, nullable=False)  # List of questions with options and correct answers
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    answers = Column(JSON, nullable=False)  # User's selected answers
    score = Column(Float, nullable=False)  # Percentage score
    is_completed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
