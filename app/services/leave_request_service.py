from app import db
from app.models import leave_request
from datetime import datetime

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

        # Chuyển đổi dữ liệu ngày sang định dạng datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Tạo yêu cầu nghỉ phép mới
        new_leave_request = leave_request(
            id_employee=id_employee,
            start_date=start_date,
            end_date=end_date,
            request_type=request_type,
            reason=reason,
            status='Pending',  # Trạng thái mặc định là "Pending"
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
