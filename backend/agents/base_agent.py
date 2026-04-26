import os
import json
import re
import time
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from groq import Groq

load_dotenv()

class BaseAgent:
    def __init__(self, prompt_path: str):
        self.primary_provider = os.getenv("LLM_PROVIDER", "groq").lower()
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def _clean_json(self, text: str) -> str:
        text = re.sub(r'```json\s*|\s*```', '', text)
        text = re.sub(r'```\s*|\s*```', '', text)
        return text.strip()

    def get_completion(self, user_content: str, system_prompt: str = None, **kwargs) -> dict:
        base_prompt = system_prompt if system_prompt else self.system_prompt
        
        # Safe formatting for prompts with JSON braces
        formatted_system_prompt = base_prompt
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            formatted_system_prompt = formatted_system_prompt.replace(placeholder, str(value))
        
        # Try providers in order: Primary -> Others as fallbacks
        providers = [self.primary_provider]
        fallbacks = ["groq", "gemini", "openai"]
        for f in fallbacks:
            if f not in providers:
                providers.append(f)
        
        last_error = None
        for provider in providers:
            try:
                print(f"INFO: Attempting completion with {provider}...")
                if provider == "openai":
                    if not os.getenv("OPENAI_API_KEY") or "your_openai" in os.getenv("OPENAI_API_KEY"):
                        continue
                    return self._openai_completion(formatted_system_prompt, user_content)
                elif provider == "gemini":
                    if not os.getenv("GEMINI_API_KEY"):
                        continue
                    return self._gemini_completion(formatted_system_prompt, user_content)
                elif provider == "groq":
                    if not os.getenv("GROQ_API_KEY"):
                        continue
                    return self._groq_completion(formatted_system_prompt, user_content)
            except Exception as e:
                last_error = str(e)
                print(f"WARNING: Provider {provider} failed: {e}. Trying next fallback...")
                continue
        
        # If all fail
        return {
            "error": True,
            "message": f"Tüm yapay zeka servisleri başarısız oldu. Son hata: {last_error}",
            "plan_name": "Servis Kesintisi",
            "overview": "Şu an tüm yapay zeka modellerimiz yoğunluk nedeniyle hizmet veremiyor.",
            "weeks": [],
            "coach_feedback": "Üzgünüm, kota sınırları aşıldığı için şu an yanıt veremiyorum.",
            "motivation_message": "Lütfen birkaç dakika sonra tekrar deneyin.",
            "actionable_steps": ["Farklı bir model seçmeyi deneyin", "Sayfayı yenileyin"]
        }

    def _openai_completion(self, system_prompt: str, user_content: str) -> dict:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini") # Use mini for better limits/speed
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )
        content = self._clean_json(response.choices[0].message.content)
        return json.loads(content)

    def _gemini_completion(self, system_prompt: str, user_content: str) -> dict:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Use flash for higher rate limits and speed
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        
        response = model.generate_content(
            user_content,
            generation_config={"response_mime_type": "application/json"}
        )
        content = self._clean_json(response.text)
        return json.loads(content)

    def _groq_completion(self, system_prompt: str, user_content: str) -> dict:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Use a model with higher rate limits (llama-3.1-8b is usually much more permissive)
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )
        content = self._clean_json(response.choices[0].message.content)
        return json.loads(content)
