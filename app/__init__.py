from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import DevelopmentConfig
from flask_socketio import SocketIO
socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes import auth, attendance, leave_request, employee,face
    app.register_blueprint(auth.bp)
    app.register_blueprint(attendance.bp)
    app.register_blueprint(leave_request.bp)
    app.register_blueprint(employee.bp)
    app.register_blueprint(face.bp)
    from app.routes.ledSetting import register_led_routes
    register_led_routes(socketio)
    return app
