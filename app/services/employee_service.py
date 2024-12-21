from flask import jsonify
from app.models import Employee
from app import db
from flask_jwt_extended import  get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
from sqlalchemy import or_
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
    if "password" in data:
        new_password=data['password']
    data['password'] = generate_password_hash(new_password)
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
        return jsonify({'error': 'Permission denied !'}), 403
# Phân trang
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 10, type=int)
    search = request.args.get('searchValue', '', type=str)

    query = Employee.query.filter(
        
        or_(
            Employee.id_employee.like(f"%{search}%"),
            Employee.name.like(f"%{search}%")
        )
    )

    paginated_employees = query.paginate(page=page, per_page=per_page, error_out=False)

    employees = paginated_employees.items
    if not employees:
        return jsonify({'error': 'No employees found'}), 404
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
            'department': {
                'name': employee.department.name if employee.department else None
            } if employee.department else None
        })
    return jsonify({
        'employees': employee_data,
        'total': paginated_employees.total,
        'pages': paginated_employees.pages,
        'current_page': paginated_employees.page
    }), 200
