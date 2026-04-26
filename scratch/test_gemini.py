import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()

def test_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    system_prompt = "Sen bir öğrenme koçusun. JSON formatında yanıt ver."
    user_content = "Python öğrenmek istiyorum. Bana bir plan yap."
    
    # Try without system_instruction first to see if it works
    response = model.generate_content(
        f"System: {system_prompt}\n\nUser: {user_content}",
        generation_config={"response_mime_type": "application/json"}
    )
    
    print("Response Text:")
    print(response.text)

if __name__ == "__main__":
    test_gemini()
