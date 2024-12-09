from app import db

class Attendance(db.Model):
    id_attendance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id_employee'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)

    employee = db.relationship('Employee', backref='attendances', lazy=True)
