import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key:str = os.getenv('JWT_SECRET_KEY')
    jwt_secret_algorithm:str = os.getenv('JWT_ALGORITHM')
    jwt_expire_minutes:str = os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')