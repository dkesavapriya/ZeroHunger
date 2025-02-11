import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Change this to a strong secret key
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/databasname")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")  # Change this for security
    SOCKETIO_MESSAGE_QUEUE = os.getenv("REDIS_URL", "redis://")  # Required for real-time notifications
    JWT_ACCESS_TOKEN_EXPIRES = False
    
