from flask import Blueprint, request, jsonify
from app.services.face_service import capture_face_data, train_model_service, log_attendance
from datetime import datetime

bp = Blueprint('face', __name__, url_prefix='/face')

@bp.route('/collect', methods=['POST'])
def collect_face():
    # Lấy ID từ yêu cầu POST
    user_id = request.json.get('id')

    if not user_id:
        return jsonify({"error": "ID không được cung cấp"}), 400

    # Thu thập dữ liệu khuôn mặt
    try:
        capture_face_data(user_id)
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
    data = request.json
    print("Received data:", data)  # Debug log
    predicted_id = data.get('id')

    if not predicted_id:
        return jsonify({"error": "Missing predicted ID."}), 400

    try:
        # Log attendance
        log_attendance(predicted_id, "checkin")
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
        # Log attendance
        log_attendance(predicted_id, "checkout")
        return jsonify({
            "message": f"Check-out successful for ID {predicted_id}.",
            "status": "checkout",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

