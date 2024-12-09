import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://user:password@localhost/face_attendance')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:trong123@localhost/face_attendance'
