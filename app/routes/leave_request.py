from flask import Blueprint, request, jsonify
from app.services.leave_request_service import request_leave

bp = Blueprint('leave_request', __name__, url_prefix='/leave_request')

@bp.route('/create', methods=['POST'])
def create_leave():
    data = request.get_json()
    return request_leave(data)
