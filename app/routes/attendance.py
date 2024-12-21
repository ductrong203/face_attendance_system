from flask import Blueprint, request, jsonify
from app.services.attendance_service import get_employee_attendance_summary,get_admin_attendance_summary
from flask_jwt_extended import jwt_required
bp = Blueprint('attendance', __name__, url_prefix='/attendance')
#Nhan vien

@bp.route('/employee/<int:id>', methods=['GET'])
def get_employee_attendance(id):
    try:
        # Lấy các tham số từ query string
        day = request.args.get('day', None)
        month = request.args.get('month', None)
        quarter = request.args.get('quarter', None)
        year = request.args.get('year', None)
        return get_employee_attendance_summary(id, day, month, quarter, year)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#admin

@bp.route('/admin/<int:id>', methods=['GET'])
@jwt_required() 
def get_admin_attendance_by_employee(id):
    try:
        # Lấy các tham số từ query string
        day = request.args.get('day', None)
        month = request.args.get('month', None)
        quarter = request.args.get('quarter', None)
        year = request.args.get('year', None)
        return  get_admin_attendance_summary(id, day, month, quarter, year)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@bp.route('/admin/summary', methods=['GET'])
@jwt_required() 
def get_admin_summary():
    try:
        # Lấy các tham số từ query string
        day = request.args.get('day', None)
        month = request.args.get('month', None)
        quarter = request.args.get('quarter', None)
        year = request.args.get('year', None)
        return  get_admin_attendance_summary(day, month, quarter, year)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
