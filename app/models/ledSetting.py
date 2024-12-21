from app import db

class LedSetting(db.Model):
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False, default="Welcome to Flask!")
    speed = db.Column(db.Integer, nullable=False, default=25)
    direction = db.Column(db.String(10), nullable=False, default="left")
    brightness = db.Column(db.Integer, nullable=False, default=5)