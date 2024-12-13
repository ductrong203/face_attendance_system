from flask import Blueprint, request, jsonify
from app.services.leave_request_service import request_leave,get_employee_leave_requests

bp = Blueprint('leave_request', __name__, url_prefix='/leave_request')
#  tạo đơn xin nghỉ.
@bp.route('/create', methods=['POST'])
def create_leave():
    data = request.get_json()
    return request_leave(data)

# Nhân viên xem đơn xin nghỉ
@bp.route('/employee_requests', methods=['GET'])
def employee_requests():
    id_employee = request.args.get('id_employee')
    if not id_employee:
        return jsonify({'error': 'Missing employee ID'}), 400

    response, status = get_employee_leave_requests(id_employee)
    return jsonify(response), status
