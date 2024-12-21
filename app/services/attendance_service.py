from flask import jsonify
from app.models import Attendance,Employee
from sqlalchemy import extract
from flask_jwt_extended import  get_jwt_identity
from datetime import datetime
# Lọc thông tin điểm danh của nhân viên theo ngày, tháng, năm
def get_employee_attendance_summary(employee_id,day=None,month=None,quarter=None, year=None):
    try:
        query = Attendance.query.filter(Attendance.id_employee == employee_id)
        if day:
            query = query.filter(extract('day', Attendance.date) == int(day))
        if month:
            query = query.filter(extract('month', Attendance.date) == int(month))
        if year:
            query = query.filter(extract('year', Attendance.date) == int(year))
        if quarter:
            query = query.filter(
                ((extract('month', Attendance.date) - 1) // 3 + 1) == int(quarter)
            )
        # Lấy dữ liệu
        attendance_data = query.all()
        if not attendance_data:
            return jsonify({'error': 'No attendance records found.'}), 404

        late_employees = len([a for a in attendance_data if a.time_in and (a.time_in.hour > 8 or (a.time_in.hour == 8 and a.time_in.minute > 30))])
        working_employees = len([a for a in attendance_data if a.time_in])
        absent_employees = len([a for a in attendance_data if not a.time_in])
        attendance_list = []
        for attendance in attendance_data:
            attendance_list.append({
                'id': attendance.id_attendance,
                'date': attendance.date.strftime('%Y-%m-%d'),
                'time_in': attendance.time_in.strftime('%H:%M:%S') if attendance.time_in else None,
                'time_out': attendance.time_out.strftime('%H:%M:%S') if attendance.time_out else None,
            })
        return jsonify({
            'summary': {
                'late': late_employees,
                'worked': working_employees,
                'absent': absent_employees
            },
            "attendance_data":attendance_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin
def get_admin_attendance_summary(employee_id=None,day=None,month=None,quarter=None, year=None):
    current_user_id = get_jwt_identity()
    current_user = Employee.query.get(current_user_id)
    if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'Permission denied !'}), 403
    try:
        query = Attendance.query   
        if employee_id:
            query = query.filter(Attendance.id_employee == employee_id)
        if day:
            query = query.filter(extract('day', Attendance.date) == int(day))
        if month:
            query = query.filter(extract('month', Attendance.date) == int(month))
        if year:
            query = query.filter(extract('year', Attendance.date) == int(year))
        if quarter:
            query = query.filter(
                ((extract('month', Attendance.date) - 1) // 3 + 1) == int(quarter)
            )
        # Lấy dữ liệu
        attendance_data = query.all()
        if not attendance_data:
            return jsonify({'error': 'No attendance records found.'}), 404

        late_employees = len([a for a in attendance_data if a.time_in and (a.time_in.hour > 8 or (a.time_in.hour == 8 and a.time_in.minute > 30))])
        working_employees = len([a for a in attendance_data if a.time_in])
        absent_employees = len([a for a in attendance_data if not a.time_in])
        attendance_list = []
        for attendance in attendance_data:
            attendance_list.append({
                'id': attendance.id_attendance,
                'date': attendance.date.strftime('%Y-%m-%d'),
                'time_in': attendance.time_in.strftime('%H:%M:%S') if attendance.time_in else None,
                'time_out': attendance.time_out.strftime('%H:%M:%S') if attendance.time_out else None,
            })
        return jsonify({
            'summary': {
                'late': late_employees,
                'worked': working_employees,
                'absent': absent_employees
            },
            "attendance_data":attendance_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500