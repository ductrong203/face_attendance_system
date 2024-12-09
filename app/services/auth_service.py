from app import db
from datetime import timedelta
from app.models.employee import Employee
from flask_jwt_extended import create_access_token,get_jwt
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from flask import Flask, request, jsonify
from app.models import BlockedToken


# đăng nhập
def login(data):
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logging.error("Missing username or password")
        return jsonify({"msg": "Username and password are required"}), 400

    user = Employee.query.filter_by(username=username).first()
    if not user:
        logging.error(f"User {username} not found")
        return jsonify({"msg": "User not found"}), 404

    if user.password is None:
        logging.error("Password hash is missing for user")
        return jsonify({"msg": "Password hash missing"}), 500

    if check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id_employee), expires_delta=timedelta(hours=1))
        logging.info(f"User {username} logged in successfully")
        return jsonify(access_token=access_token), 200

    logging.warning("Invalid credentials")
    return jsonify({"msg": "Invalid credentials"}), 401

# đăng ký
def register(data):
    required_fields = ['id_employee','username', 'password', 'name', 'email', 'gender', 'phone', 'role', 'address', 'id_department']
    
    # Kiểm tra các trường bắt buộc
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required"}), 400  

    # Kiểm tra trùng lặp username hoặc email
    if Employee.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    if Employee.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400

    # Mã hóa mật khẩu
    hashed_password = generate_password_hash(data['password'])

    # Tạo người dùng mới
    new_user = Employee(
        id_employee=data['id_employee'],
        username=data['username'],
        password=hashed_password,
        name=data['name'],
        email=data['email'],
        gender=data['gender'],
        phone=data['phone'],
        role=data['role'],
        address=data['address'],
        isAdmin=data.get('isAdmin', False),  # Thiết lập isAdmin mặc định là False nếu không có
        id_department=data['id_department']
    )
    
    # Thêm người dùng vào cơ sở dữ liệu
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

# đăng xuất

def logout_user():
    try:
        jti = get_jwt()['jti']  # Lấy JWT ID từ token

        # Lưu token vào bảng blocked_tokens
        blocked_token = BlockedToken(jti=jti)
        db.session.add(blocked_token)
        db.session.commit()

        return {"msg": "Successfully logged out"}, 200
    except Exception as e:
        return {"msg": f"An error occurred during logout: {str(e)}"}, 500