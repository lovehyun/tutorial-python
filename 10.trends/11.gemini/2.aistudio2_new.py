# pip install google-genai
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="안녕하세요"
)

print(response.text)
