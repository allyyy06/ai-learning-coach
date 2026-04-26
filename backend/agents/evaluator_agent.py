from .base_agent import BaseAgent
import os

class EvaluatorAgent(BaseAgent):
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "../../prompts/evaluator_prompt.txt")
        super().__init__(prompt_path)

    def evaluate_progress(self, goal: str, progress_report: str):
        return self.get_completion(
            progress_report,
            goal=goal,
            progress_report=progress_report
        )

    def generate_quiz(self, goal: str, content: str, topic: str = "Bilinmiyor"):
        prompt_path = os.path.join(os.path.dirname(__file__), "../../prompts/quiz_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            quiz_system_prompt = f.read()
        
        return self.get_completion(
            f"Lütfen şu konu ve içerik için 3 soruluk quiz oluştur: Konu: {topic}, İçerik: {content}",
            system_prompt=quiz_system_prompt,
            goal=goal,
            topic=topic,
            content=content
        )
