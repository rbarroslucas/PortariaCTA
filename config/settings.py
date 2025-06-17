import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALG = os.getenv("ALG")
ACCESS_TOKEN_DURATION = int(os.getenv("ACCESS_TOKEN_DURATION"))
API_URL = os.getenv("API_URL")