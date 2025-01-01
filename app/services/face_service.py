from app.models.face import Face  # Import model Face
from app import db  # Import SQLAlchemy instance
import cv2
import numpy as np
import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from win32com.client import Dispatch
from datetime import datetime
import base64
from app.models.attendance import Attendance
# thu thap du lieu khuon mat
def capture_face_data(user_id, face_base64):
    # Chuyển đổi dữ liệu base64 thành ảnh
    faces_data = []
    for face_b64 in face_base64:
        img_data = base64.b64decode(face_b64)
        np_arr = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        faces_data.append(img)

    # Lưu dữ liệu vào cơ sở dữ liệu
    try:
        for face in faces_data:
            encoded_data = pickle.dumps(face)  # Mã hóa dữ liệu khuôn mặt bằng pickle
            face_entry = Face(id_employee=user_id, face_data=encoded_data)
            db.session.add(face_entry)
            db.session.commit()
            print(f"Dữ liệu khuôn mặt đã được lưu thành công cho user_id {user_id}.")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu vào cơ sở dữ liệu: {e}")
        db.session.rollback()


# Hàm tiền xử lý dữ liệu
def fetch_training_data():
    results = Face.query.all()
    
    X = []
    y = []

    for row in results:
        try:
            image_data = pickle.loads(row.face_data)
            label = row.id_employee
            X.append(image_data)
            y.append(label)
        except Exception as e:
            print(f"Error processing row {row}: {e}")

    print(f"Fetched {len(X)} samples with {len(y)} labels.")
    return X, y



# Hàm huấn luyện mô hình
def train_model_service():

    faces, labels = fetch_training_data()
    faces = np.asarray(faces)
    faces = faces.reshape(faces.shape[0], -1)

 
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

  
    X_train, X_test, y_train, y_test = train_test_split(
        faces, labels, test_size=0.2, random_state=42
    )


    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train, y_train)

    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    with open(r'C:\Desktop\face_attendance_system\data\svm_model\svm_model.pkl', 'wb') as f:
        pickle.dump(svm_model, f)
    with open(r'C:\Desktop\face_attendance_system\data\svm_model\label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    return accuracy


def log_attendance(predicted_id, status):
    date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")

    if status == "checkin":
        # Kiểm tra xem nhân viên đã điểm danh vào ngày hôm nay chưa
        attendance = Attendance.query.filter_by(id_employee=predicted_id, date=date).first()
        
        if not attendance:
            # Nếu chưa, tạo mới bản ghi attendance
            new_attendance = Attendance(
                id_employee=predicted_id,
                date=date,
                time_in=timestamp
            )
            db.session.add(new_attendance)
            db.session.commit()

    elif status == "checkout":
        # Cập nhật giờ ra nếu đã có bản ghi attendance cho ngày hôm nay
        attendance = Attendance.query.filter_by(id_employee=predicted_id, date=date).first()
        
        if attendance:
            attendance.time_out = timestamp
            db.session.commit()


