import requests
from schemas import DwellerSchema

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQ5NzgwMTg5fQ.zG7OuW7UKKUJtdn8UIez4gcVeo553NcmT21vyvCGUr4"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


dweller = DwellerSchema(
    name="Alice",
    email="alice@example.com",
    cpf="52998224725",
    password="securepassword123",
    active=True,
    admin=False
)

#request = requests.get(
#    "http://127.0.0.1:8000/auth/refresh",
#    headers=headers
#)

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
print("Conectado com sucesso!")
conn.close()
