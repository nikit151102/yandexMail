import os
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def verify_credentials(credentials: HTTPBasicCredentials):
    correct_username = (credentials.username == USERNAME)
    correct_password = (credentials.password == PASSWORD)
    
    print(USERNAME, PASSWORD)

    print(credentials.username, credentials.password)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Basic"},
        )
