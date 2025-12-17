import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    @staticmethod
    def validate():
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in .env file.")