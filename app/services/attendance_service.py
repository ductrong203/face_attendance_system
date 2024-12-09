from app import db
from app.models.attendance import Attendance

def mark_attendance(data):
    new_attendance = Attendance(id_employee=data['id_employee'], date=data['date'], time_in=data['time_in'], time_out=data['time_out'])
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({"msg": "Attendance marked successfully"}), 200
