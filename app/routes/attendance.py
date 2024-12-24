from flask import Blueprint, request, jsonify
from app.services.attendance_service import get_employee_attendance_summary,get_admin_attendance_summary
from flask_jwt_extended import jwt_required
bp = Blueprint('attendance', __name__, url_prefix='/attendance')
#Nhan vien

@bp.route('/employee/<int:id>', methods=['GET'])
def get_employee_attendance(id):
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        return get_employee_attendance_summary(id, start_date, end_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# adminadmin
@bp.route('/admin/<int:id>', methods=['GET'])
@jwt_required()
def get_admin_attendance_by_employee(id):
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        return get_admin_attendance_summary(id, start_date, end_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/summary', methods=['GET'])
@jwt_required()
def get_admin_summary():
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        return get_admin_attendance_summary(None, start_date, end_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
