import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

def test_groq():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Sen bir öğrenme koçusun. JSON formatında yanıt ver."},
                {"role": "user", "content": "Python öğrenmek istiyorum. Bana bir plan yap."}
            ],
            response_format={"type": "json_object"}
        )
        print("Response Content:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_groq()
