from flask import Blueprint, request, jsonify
from app.services.face_service import capture_face_data,train_model_service
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
        return jsonify({"message": "Dữ liệu khuôn mặt đã được thu thập cho ID {}".format(user_id)}), 200
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