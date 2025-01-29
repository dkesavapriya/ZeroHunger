from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    CORS(app)

    # Import and register blueprints inside the function to avoid circular imports
    from app.routes import volunteer_bp, recipient_bp, donation_bp, auth_bp, dashboard_bp
    from app.notifications import notify_nearby_users
    app.register_blueprint(volunteer_bp, url_prefix='/api/volunteers')
    app.register_blueprint(recipient_bp, url_prefix='/api/recipients')
    app.register_blueprint(donation_bp, url_prefix='/api/donations')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app
