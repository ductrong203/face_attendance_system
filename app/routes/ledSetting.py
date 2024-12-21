from flask import Blueprint, request, jsonify
from app.services.ledSetting_service import (
    get_current_message,
    update_message_in_db,
    update_speed_in_db,
    update_direction_in_db,
    update_brightness_in_db
)

bp = Blueprint('led', __name__, url_prefix='/led')

@bp.route('/message', methods=['GET'])
def get_message():
    message = get_current_message()
    return jsonify({"message": message})

@bp.route('/message_update', methods=['PUT'])
def update_led_message():
    data = request.get_json()
    message = data.get('message', 'Welcome to Flask!')
    if not message:
        return jsonify({"status": "error", "message": "Message content is required"}), 400

    updated_message = update_message_in_db(message)
    return jsonify({"status": "success", "new_message": updated_message})

@bp.route('/speed', methods=['PUT'])
def update_led_speed():
    """
    Cập nhật tốc độ trong cơ sở dữ liệu.
    """
    data = request.get_json()
    speed = data.get('speed', 25)
    if not isinstance(speed, int) or speed <= 0:
        return jsonify({"status": "error", "message": "Invalid speed value"}), 400

    updated_speed = update_speed_in_db(speed)
    return jsonify({"status": "success", "new_speed": updated_speed})

@bp.route('/direction', methods=['PUT'])
def update_led_direction():
    """
    Cập nhật hướng trong cơ sở dữ liệu.
    """
    data = request.get_json()
    direction = data.get('direction', 'left')
    if direction not in ['left', 'right']:
        return jsonify({"status": "error", "message": "Invalid direction value"}), 400

    updated_direction = update_direction_in_db(direction)
    return jsonify({"status": "success", "new_direction": updated_direction})

@bp.route('/brightness', methods=['PUT'])
def update_led_brightness():
    """
    Cập nhật độ sáng trong cơ sở dữ liệu.
    """
    data = request.get_json()
    brightness = data.get('brightness', 5)
    if not isinstance(brightness, int) or brightness < 1 or brightness > 10:
        return jsonify({"status": "error", "message": "Brightness must be between 1 and 10"}), 400

    updated_brightness = update_brightness_in_db(brightness)
    return jsonify({"status": "success", "new_brightness": updated_brightness})
