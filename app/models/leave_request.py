from app import db

class LeaveRequest(db.Model):
    id_leave = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id_employee'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20))
    request_type = db.Column(db.Text)
    reason = db.Column(db.Text)
    request_date = db.Column(db.Date, nullable=False)

    employee = db.relationship('Employee', backref='leave_requests', lazy=True)
