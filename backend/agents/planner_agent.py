from .base_agent import BaseAgent
import os

class PlannerAgent(BaseAgent):
    def __init__(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "../../prompts/planner_prompt.txt")
        super().__init__(prompt_path)

    def generate_plan(self, goal: str, level: str, daily_time: int, learning_style: str):
        user_content = f"Lütfen benim için {goal} hedefli bir plan oluştur."
        return self.get_completion(
            user_content,
            goal=goal,
            level=level,
            daily_time=daily_time,
            learning_style=learning_style
        )

    def update_plan(self, current_plan: dict, performance_summary: str):
        # Adaptive logic: update plan based on performance
        user_content = f"Mevcut planım: {current_plan}. Son performans özetim: {performance_summary}. Lütfen planı buna göre güncelle."
        # Using the same system prompt but we can add more logic if needed
        return self.get_completion(
            user_content,
            goal="Mevcut Hedef", # We might need to pass actual goal here
            level="Dinamik",
            daily_time=60,
            learning_style="Dinamik"
        )
