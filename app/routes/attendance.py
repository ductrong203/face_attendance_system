from flask import Blueprint, request, jsonify
from app.services.attendance_service import mark_attendance

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/<int:number>', methods=['POST'])
def mark():
    data = request.get_json()
    return mark_attendance(data)
