from flask import Blueprint, request, jsonify
from app import db, jwt
from app.models.employee import Employee
from app.services.auth_service import login, register,logout_user
from flask_jwt_extended import jwt_required
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return login(data)

@bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    return register(data)
#logout
@bp.route('/logout', methods=['POST'])
@jwt_required()  # Đảm bảo người dùng đã đăng nhập mới có thể đăng xuất
def logout():
    response = logout_user()  # Gọi service logout_user
    return jsonify(response)