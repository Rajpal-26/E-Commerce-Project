from datetime import timedelta
import http
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/db_name")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Required for session management (used in Gmail OAuth)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-prod")

    # redis url for caching and other uses; default to localhost for local dev
    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 15)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7)))

    # CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    # CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    # REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    
    CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI")