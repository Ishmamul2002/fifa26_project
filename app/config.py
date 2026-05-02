import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fifa2026-super-secret-key-2026'
    
    # Change this to your actual database name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/fifa26_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False