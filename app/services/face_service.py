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
import cv2
import pickle
from win32com.client import Dispatch

# thu thap du lieu khuon mat
def capture_face_data(user_id):
    # Khởi động webcam và thu thập dữ liệu khuôn mặt
    video = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Kiểm tra xem webcam có mở thành công hay không
    if not video.isOpened():
        raise Exception("Không thể truy cập camera. Vui lòng kiểm tra kết nối webcam.")

    faces_data = []
    i = 0

    try:
        while True:
            ret, frame = video.read()
            frame = cv2.flip(frame, 1)  # Lật khung hình theo chiều ngang
            if not ret:
                raise Exception("Không thể đọc khung hình từ camera.")

            # Chuyển khung hình sang grayscale để phát hiện khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w]
                resized_img = cv2.resize(crop_img, (128, 128))  # Kích thước phù hợp cho mô hình SVM
                if i % 10 == 0:  # Chỉ lưu mỗi 10 khung hình để tránh trùng lặp quá nhiều
                    faces_data.append(resized_img)
                i += 1

                # Vẽ hình chữ nhật quanh khuôn mặt
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

            # Hiển thị khung hình
            cv2.imshow("Collecting faces", frame)

            # Thoát nếu đã thu thập đủ dữ liệu khuôn mặt hoặc người dùng nhấn 'q'
            if len(faces_data) >= 50:
                print("Đã thu thập đủ dữ liệu khuôn mặt.")
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Người dùng đã thoát.")
                break

    finally:
        # Giải phóng tài nguyên
        video.release()
        cv2.destroyAllWindows()

    # Lưu dữ liệu vào cơ sở dữ liệu
    try:
        for face in faces_data:
            encoded_data = pickle.dumps(face)  # Mã hóa dữ liệu bằng pickle
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
            # Giải mã dữ liệu khuôn mặt
            image_data = pickle.loads(row.face_data)
            label = row.id_employee

            # Thêm vào danh sách
            X.append(image_data)
            y.append(label)
        except Exception as e:
            print(f"Error processing row {row}: {e}")

    print(f"Fetched {len(X)} samples with {len(y)} labels.")
    return X, y



# Hàm huấn luyện mô hình
def train_model_service():
    # Fetch training data
    faces, labels = fetch_training_data()
    faces = np.asarray(faces)
    faces = faces.reshape(faces.shape[0], -1)

    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        faces, labels, test_size=0.2, random_state=42
    )

    # Train the SVM model
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Save the model and label encoder
    with open(r'C:\Desktop\face_attendance_system\data\svm_model\svm_model.pkl', 'wb') as f:
        pickle.dump(svm_model, f)
    with open(r'C:\Desktop\face_attendance_system\data\svm_model\label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    return accuracy

