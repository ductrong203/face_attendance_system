from app import db

class Department(db.Model):
    id_department = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    department_function = db.Column(db.String(100))

