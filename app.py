from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Cấu hình CORS cho toàn bộ ứng dụng, cho phép mọi nguồn gốc (origins)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    # Thêm headers CORS vào phản hồi
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

@app.route('/')
def home():
    return jsonify(message="Hello, World!")


app.run(debug=True)


