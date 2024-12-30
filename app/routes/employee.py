from flask import Blueprint, request, jsonify
from app.services.employee_service import get_employee_info, updated_employee_info,delete_employee_info,get_all_employee_info
from flask_jwt_extended import jwt_required
bp = Blueprint('employee', __name__, url_prefix='/employee')
# Lấy thông tin nhân viên
@bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    return get_employee_info(id)

@bp.route('/update/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    return updated_employee_info(id, data)
@bp.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_employee(id):
      return delete_employee_info(id)
@bp.route('/getAll', methods=['GET'])
@jwt_required()
def get_all_employee():
     return get_all_employee_info()
     
