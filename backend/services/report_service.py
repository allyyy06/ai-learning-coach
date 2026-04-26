from sqlalchemy.orm import Session
from ..database.models import PerformanceReport, DailyProgress, UserProfile
from ..agents.coach_agent import CoachAgent
from datetime import datetime, timedelta
import json

coach = CoachAgent()

def generate_weekly_report(db: Session, user_id: int):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        return None

    # Get progress from last 7 days
    last_week = datetime.utcnow() - timedelta(days=7)
    progress_entries = db.query(DailyProgress).filter(
        DailyProgress.user_id == user_id,
        DailyProgress.date >= last_week
    ).all()
    
    if not progress_entries:
        return None
    
    # Prepare data for AI analysis
    progress_summary = []
    for p in progress_entries:
        progress_summary.append({
            "date": p.date.strftime("%Y-%m-%d"),
            "content": p.content,
            "score": p.performance_score,
            "feedback": p.feedback
        })
    
    scores = [p.performance_score for p in progress_entries if p.performance_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Use AI to generate an insightful summary and suggestions
    user_context = {
        "full_name": user.full_name,
        "goal": user.goal,
        "level": user.level
    }
    
    prompt = f"""
    Aşağıda kullanıcının son bir haftalık öğrenme verileri yer almaktadır:
    {json.dumps(progress_summary, ensure_ascii=False)}
    
    Lütfen bu verileri analiz ederek:
    1. Haftalık genel bir başarı özeti yaz.
    2. Kullanıcının güçlü olduğu ve gelişmesi gereken noktaları belirt.
    3. Gelecek hafta için 3 spesifik ve aksiyon alınabilir öneri sun.
    
    Yanıtı şu formatta JSON olarak ver:
    {{
        "summary": "...",
        "suggestions": ["...", "...", "..."]
    }}
    """
    
    ai_response = coach.get_completion(
        prompt,
        evaluation_results="Haftalık Analiz",
        user_profile=user_context
    )
    
    report = PerformanceReport(
        user_id=user_id,
        report_type="weekly",
        summary=ai_response.get("summary", "Haftalık özet oluşturulamadı."),
        metrics={
            "ortalama_puan": round(avg_score, 1),
            "aktif_gün_sayısı": len(progress_entries),
            "toplam_kayıt": len(progress_entries)
        },
        suggestions=ai_response.get("suggestions", ["Düzenli çalışmaya devam edin."])
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_reports(db: Session, user_id: int):
    return db.query(PerformanceReport).filter(PerformanceReport.user_id == user_id).order_by(PerformanceReport.created_at.desc()).all()
