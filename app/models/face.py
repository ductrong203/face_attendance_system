from app import db

class Face(db.Model):
    id_face = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id_employee'), nullable=False)
    face_data = db.Column(db.LargeBinary)  # Lưu dữ liệu ảnh khuôn mặt

    employee = db.relationship('Employee', backref='faces', lazy=True)
