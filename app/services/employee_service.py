from flask import jsonify
from app.models import Employee
from app import db
from flask_jwt_extended import  get_jwt_identity
# Lấy thông tin nhân viên 
def get_employee_info(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    department_name = employee.department.name if employee.department else None
    employee_data = {
        'id': employee.id_employee,
        'name': employee.name,
        'gender': employee.gender,
        'email': employee.email,
        'phone': employee.phone,
        'role': employee.role,
        'address': employee.address,
        'isAdmin': employee.isAdmin,
        'department': department_name
    }
    return jsonify({'employee': employee_data}), 200
# Sửa thông tin nhân viên
def updated_employee_info(employee_id, data):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    # Kiểm tra nếu mật khẩu mới được gửi trong data
    if 'password' in data:
        new_password = data['password']
        if employee.password == new_password:
            return jsonify({'error': 'New password cannot be the same as the old password'}), 400

    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
    try:
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
#xoa nhan vien
def delete_employee_info(employee_id):
    current_user_id = get_jwt_identity()
    current_user = Employee.query.get(current_user_id)
    if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'You do not have permission to delete employees'}), 403
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# Xem tất cả tt nhân viên
def get_all_employee_info():
     current_user_id = get_jwt_identity()
     current_user = Employee.query.get(current_user_id)
     if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'You do not have permission to get all employees'}), 403
     employees = Employee.query.all()
     if not employees:
          return jsonify({'error': 'There are no employees'}), 404
     employee_data = []
     for employee in employees:
        employee_data.append({
            'id': employee.id_employee,
            'username': employee.username,
            'name': employee.name,
            'email': employee.email,
            'gender': employee.gender,
            'phone': employee.phone,
            'role': employee.role,
            'address': employee.address,
            'isAdmin': employee.isAdmin,
            'department': employee.department.name if employee.department else None
        })
        return jsonify({'employees': employee_data}), 200