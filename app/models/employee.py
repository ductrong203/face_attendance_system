from app import db

class Employee(db.Model):
    id_employee = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    role = db.Column(db.String(15))
    address = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Password mã hóa
    isAdmin = db.Column(db.Boolean, default=False)
    id_department = db.Column(db.Integer, db.ForeignKey('department.id_department'))
    

    department = db.relationship('Department', backref='employees', lazy=True)
