from app.models import  LedSetting
from app import db
def get_current_message():
 
    led_setting = LedSetting.query.first()
    return led_setting.message if led_setting else "Welcome to Flask!"

def update_message_in_db(new_message):

    led_setting = LedSetting.query.first()
    if not led_setting:
        led_setting = LedSetting(message=new_message)
        db.session.add(led_setting)
    else:
        led_setting.message = new_message

    db.session.commit()
    return led_setting.message

def update_speed_in_db(new_speed):
 
    led_setting = LedSetting.query.first()
    if not led_setting:
        led_setting = LedSetting(speed=new_speed)
        db.session.add(led_setting)
    else:
        led_setting.speed = new_speed

    db.session.commit()
    return led_setting.speed

def update_direction_in_db(new_direction):

    led_setting = LedSetting.query.first()
    if not led_setting:
        led_setting = LedSetting(direction=new_direction)
        db.session.add(led_setting)
    else:
        led_setting.direction = new_direction

    db.session.commit()
    return led_setting.direction

def update_brightness_in_db(new_brightness):
  
    led_setting = LedSetting.query.first()
    if not led_setting:
        led_setting = LedSetting(brightness=new_brightness)
        db.session.add(led_setting)
    else:
        led_setting.brightness = new_brightness

    db.session.commit()
    return led_setting.brightness
