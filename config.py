import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    DATABASE_URI = os.getenv('DATABASE_URI', 'database.db')
