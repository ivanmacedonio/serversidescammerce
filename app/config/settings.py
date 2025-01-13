import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key:str = os.getenv('JWT_SECRET_KEY')
    jwt_secret_algorithm:str = os.getenv('JWT_ALGORITHM')
    jwt_expire_minutes:str = os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
    telegram_token:str = os.getenv('TELEGRAM_TOKEN')
    api_key:str = os.getenv('API_KEY')
    pg_username:str = os.getenv('PG_USERNAME')
    pg_password:str = os.getenv('PG_PASSWORD')
    pg_host:str = os.getenv('PG_HOST')
    pg_port:str = os.getenv('PG_PORT')
    pg_db_name:str = os.getenv('PG_DB_NAME')