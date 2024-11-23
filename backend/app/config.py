# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # AWS
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    AWS_REGION = os.environ.get('AWS_REGION', 'sa-east-1')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5434/video_platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB limit