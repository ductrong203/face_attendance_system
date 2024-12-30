from app.models import LedSetting
from app import db

def get_current_message():
    setting = LedSetting.query.first()
    return setting.message if setting else "Welcome to Flask!"

def update_message(new_message):
    setting = LedSetting.query.first()
    if not setting:
        setting = LedSetting(message=new_message)
        db.session.add(setting)
    else:
        setting.message = new_message
    db.session.commit()
    return setting.message
