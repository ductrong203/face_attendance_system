from flask_socketio import emit
from app.services.ledSetting_service import get_current_message, update_message

def register_led_routes(socketio):
    @socketio.on('connect')
    def handle_connect():
        """Xử lý khi client kết nối."""
        emit('status', {'message': 'Connected to WebSocket server'})

    @socketio.on('get_message')
    def handle_get_message():
        """Lấy tin nhắn hiện tại."""
        message = get_current_message()
        emit('message', {'message': message})

    @socketio.on('update_message')
    def handle_update_message(data):
        """Cập nhật tin nhắn."""
        new_message = data.get('message', 'Welcome to Flask!')
        if not new_message:
            emit('error', {'message': 'Message content is required'})
            return
        updated_message = update_message(new_message)
        emit('update_message', {'new_message': updated_message})
