import os

class Config:
    SECRET_KEY = 'your_secret_key'
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
