from flask import Blueprint, request, jsonify
from app.services.face_service import capture_face_data, train_model_service, log_attendance
from datetime import datetime
import requests
bp = Blueprint('face', __name__, url_prefix='/face')
ESP32_URL = "http://172.20.10.3/open-door"  
def notify_esp32():
    try:
        response = requests.post(ESP32_URL, timeout=10)  # Gửi tín hiệu mở cửa
        if response.status_code == 200:
            print("ESP32 notified successfully.")
        else:
            print(f"Failed to notify ESP32. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error notifying ESP32: {e}")
@bp.route('/collect', methods=['POST'])
def collect_face():
    user_id = request.json.get('id')
    face_base64 = request.json.get('faces')
    
    if not user_id or not face_base64:
        return jsonify({"error": "ID hoặc dữ liệu khuôn mặt không được cung cấp"}), 400

    try:
        capture_face_data(user_id, face_base64)
        return jsonify({"message": f"Dữ liệu khuôn mặt đã được thu thập cho ID {user_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/train', methods=['POST'])
def start_training():
    try:
        accuracy = train_model_service()
        return jsonify({
            "message": "Training completed successfully.",
            "accuracy": f"{accuracy * 100:.2f}%"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/checkin', methods=['POST'])
def checkin():
    global door_status
    data = request.json
    print("Received data:", data)  
    predicted_id = data.get('id')

    if not predicted_id:
        return jsonify({"error": "Missing predicted ID."}), 400

    try:
       
        log_attendance(predicted_id, "checkin")
        notify_esp32() 
        return jsonify({
            "message": f"Check-in successful for ID {predicted_id}.",
            "status": "checkin",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    print("Received data:", data)  # Debug log
    predicted_id = data.get('id')

    if not predicted_id:
        return jsonify({"error": "Missing predicted ID."}), 400

    try:
        log_attendance(predicted_id, "checkout")
        notify_esp32() 
        return jsonify({
            "message": f"Check-out successful for ID {predicted_id}.",
            "status": "checkout",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

