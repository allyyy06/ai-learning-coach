from .base_agent import BaseAgent
import os

class CoachAgent(BaseAgent):
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "../../prompts/coach_prompt.txt")
        super().__init__(prompt_path)

    def give_feedback(self, evaluation_results: dict, user_profile: dict):
        return self.get_completion(
            f"Değerlendirme: {evaluation_results}",
            evaluation_results=evaluation_results,
            user_profile=user_profile
        )

    def answer_question(self, question: str, user_profile: dict, current_plan: str = "Bilinmiyor", recent_progress: str = "Henüz kayıt yok"):
        prompt_path = os.path.join(os.path.dirname(__file__), "../../prompts/qa_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            qa_system_prompt = f.read()
        
        return self.get_completion(
            f"Öğrenci Sorusu: {question}",
            system_prompt=qa_system_prompt,
            user_profile=user_profile,
            current_plan=current_plan,
            recent_progress=recent_progress
        )
