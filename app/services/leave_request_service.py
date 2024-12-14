from app import db
from app.models import LeaveRequest,Employee
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import  get_jwt_identity
def request_leave(data):
    try:
        # Lấy thông tin từ dữ liệu yêu cầu
        id_employee = data.get('id_employee')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        request_type = data.get('request_type')
        reason = data.get('reason')
        
        # Kiểm tra xem các trường bắt buộc có tồn tại không
        if not all([id_employee, start_date, end_date, request_type, reason]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Kiểm tra xem id_employee đã được đăng ký chưa
        employee = Employee.query.filter_by(id_employee=id_employee).first()  # Tìm nhân viên trong bảng Employee
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        # Chuyển đổi dữ liệu ngày sang định dạng datetime
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Invalid date format: {e}'}), 400

        # Tạo yêu cầu nghỉ phép mới
        new_leave_request = LeaveRequest(
            id_employee=id_employee,
            start_date=start_date,
            end_date=end_date,
            request_type=request_type,
            reason=reason,
            status='depending',  # Trạng thái mặc định là "Sent"
            request_date=datetime.now()
        )

        # Thêm yêu cầu vào cơ sở dữ liệu
        db.session.add(new_leave_request)
        db.session.commit()

        return jsonify({'message': 'Leave request created successfully'}), 201

    except Exception as e:
        # Xử lý lỗi chung
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# Nhân viên xem đơn xin nghỉ của mình
def get_employee_leave_requests(id_employee):
    try:
        requests = LeaveRequest.query.filter_by(id_employee=id_employee).all()
        if not requests:
            return {'message': 'No leave requests found'}, 404
        
        result = [{
            'id': req.id_leave,
            'start_date': req.start_date.strftime('%Y-%m-%d'),
            'end_date': req.end_date.strftime('%Y-%m-%d'),
            'request_type': req.request_type,
            'reason': req.reason,
            'status': req.status,
            'request_date': req.request_date.strftime('%Y-%m-%d %H:%M:%S')
        } for req in requests]

        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500
# admin xem tất cả đơn
def get_all_leave_requests():
    current_user_id = get_jwt_identity()
    current_user = Employee.query.get(current_user_id)
    if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'Permisstion denied !'}), 403
    try:

        requests = LeaveRequest.query.all()
        if not requests:
            return {'message': 'No leave requests found'}, 404

        result = []
        for req in requests:
            result.append({
                'id': req.id_leave,
                'id_employee': req.id_employee,
                'start_date': req.start_date.strftime('%Y-%m-%d'),
                'end_date': req.end_date.strftime('%Y-%m-%d'),
                'request_type': req.request_type,
                'reason': req.reason,
                'status': req.status,
                'request_date': req.request_date.strftime('%Y-%m-%d %H:%M:%S')
            })

        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500
# admin duyệt đơn
def update_leave_request_status(request_id, status):
    current_user_id = get_jwt_identity()
    current_user = Employee.query.get(current_user_id)
    if not current_user or not current_user.isAdmin:
        return jsonify({'error': 'Permisstion denied !'}), 403
    try:
        request_to_update = LeaveRequest.query.get(request_id)
        if not request_to_update:
            return {'error': 'Leave request not found'}, 404

        if request_to_update.status in ['Approved', 'Rejected']:
            return {'error': 'Leave request has already been processed'}, 400

        request_to_update.status = status
        db.session.commit()

        return {'message': f'Leave request {status.lower()} successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


