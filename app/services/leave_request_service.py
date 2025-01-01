from app import db
from app.models import LeaveRequest,Employee
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import  get_jwt_identity
from flask import request
def request_leave(data):
    try:
        id_employee = data.get('id_employee')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        request_type = data.get('request_type')
        reason = data.get('reason')
        if not all([id_employee, start_date, end_date, request_type, reason]):
            return jsonify({'error': 'Missing required fields'}), 400
        employee = Employee.query.filter_by(id_employee=id_employee).first()  
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Invalid date format: {e}'}), 400
        new_leave_request = LeaveRequest(
            id_employee=id_employee,
            start_date=start_date,
            end_date=end_date,
            request_type=request_type,
            reason=reason,
            status='depending',  
            request_date=datetime.now()
        )
        db.session.add(new_leave_request)
        db.session.commit()

        return jsonify({'message': 'Leave request created successfully'}), 201

    except Exception as e:
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
def get_leave_requests_by_id(request_id):
    try:
        requests = LeaveRequest.query.filter_by(id_leave=request_id).all()
        if not requests:
            return {'message': 'No leave requests found'}, 404
        
        result = [{
            'id': req.id_leave,
            'name': req.employee.name,
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
        return jsonify({'error': 'Permission denied !'}), 403
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 10, type=int)
    search = request.args.get('searchValue', '', type=str)

    try:
        query = LeaveRequest.query.join(Employee).filter(
            (
                LeaveRequest.id_employee.like(f"%{search}%"),
                Employee.name.like(f"%{search}%"),
                LeaveRequest.reason.like(f"%{search}%"),
                LeaveRequest.request_type.like(f"%{search}%")
            )
        )
        paginated_requests = query.paginate(page=page, per_page=per_page, error_out=False)
        leave_requests = paginated_requests.items

        if not leave_requests:
            return jsonify({'error': 'No leave requests found'}), 404

        result = []
        for req in leave_requests:
            result.append({
                'id': req.id_leave,
                'id_employee': req.id_employee,
                'name': req.employee.name,
                'start_date': req.start_date.strftime('%Y-%m-%d'),
                'end_date': req.end_date.strftime('%Y-%m-%d'),
                'request_type': req.request_type,
                'reason': req.reason,
                'status': req.status,
                'request_date': req.request_date.strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify({
            'leave_requests': result,
            'total': paginated_requests.total,
            'pages': paginated_requests.pages,
            'current_page': paginated_requests.page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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


