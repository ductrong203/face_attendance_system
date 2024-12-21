from flask import jsonify
from app.models import Attendance, Employee
from sqlalchemy import func, and_
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func, and_
from datetime import datetime
from app import db
def get_employee_attendance_summary(employee_id, day=None, month=None, quarter=None, year=None):
    try:
        query = Attendance.query.filter(Attendance.id_employee == employee_id)

        if day:
            query = query.filter(func.DAY(Attendance.date) == int(day))
        if month and year:
            query = query.filter(
                and_(
                    func.MONTH(Attendance.date) == int(month),
                    func.YEAR(Attendance.date) == int(year)
                )
            )
        elif month: 
            current_year = datetime.now().year
            query = query.filter(
                and_(
                    func.MONTH(Attendance.date) == int(month),
                    func.YEAR(Attendance.date) == current_year
                )
            )
        if year and not month:
            query = query.filter(func.YEAR(Attendance.date) == int(year))

        if quarter:
            quarter_months = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            query = query.filter(func.MONTH(Attendance.date).in_(quarter_months.get(int(quarter), [])))
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
            "attendance_data": attendance_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# admin
def get_admin_attendance_summary(id=None, day=None, month=None, quarter=None, year=None):
    current_user_id = get_jwt_identity()
    current_user = Employee.query.get(current_user_id)
    if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'Permission denied!'}), 403

    try:
        query = db.session.query(Attendance, Employee).join(Employee, Attendance.id_employee == Employee.id_employee)

        if id:
            query = query.filter(Attendance.id_employee == id)

        if day:
            query = query.filter(func.DAY(Attendance.date) == int(day))

        if month and year:
            query = query.filter(
                and_(
                    func.MONTH(Attendance.date) == int(month),
                    func.YEAR(Attendance.date) == int(year)
                )
            )
        elif month:
            current_year = datetime.now().year
            query = query.filter(
                and_(
                    func.MONTH(Attendance.date) == int(month),
                    func.YEAR(Attendance.date) == current_year
                )
            )
        
        if year and not month:
            query = query.filter(func.YEAR(Attendance.date) == int(year))

        # Lọc theo quý
        if quarter:
            quarter_months = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            query = query.filter(func.MONTH(Attendance.date).in_(quarter_months.get(int(quarter), [])))
        attendance_data = query.all()

        if not attendance_data:
            return jsonify({'error': 'No attendance records found.'}), 404
        total_employees = len(attendance_data)
        late_employees = len([a for a, e in attendance_data if a.time_in and (a.time_in.hour > 8 or (a.time_in.hour == 8 and a.time_in.minute > 30))])
        working_employees = len([a for a, e in attendance_data if a.time_in])
        absent_employees = len([a for a, e in attendance_data if not a.time_in])
        attendance_list = []
        for attendance, employee in attendance_data:
            attendance_list.append({
                'id': attendance.id_attendance,
                'id_employee': attendance.id_employee,
                'employee_name': employee.name if employee else 'Unknown',  
                'date': attendance.date.strftime('%Y-%m-%d'),
                'time_in': attendance.time_in.strftime('%H:%M:%S') if attendance.time_in else None,
                'time_out': attendance.time_out.strftime('%H:%M:%S') if attendance.time_out else None,
            })

        return jsonify({
            'summary': {
                'total': total_employees,
                'late': late_employees,
                'worked': working_employees,
                'absent': absent_employees
            },
            "attendance_data": attendance_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
