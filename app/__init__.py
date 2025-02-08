"""from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from .config import Config

# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="http://127.0.0.1:5000")



def create_app():
    app = Flask(__name__,template_folder="templates")
    app.config.from_object(Config)
    

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    socketio.init_app(app)

    #from app.models import User

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.volunteer import volunteer_bp
    from app.routes.recipient import recipient_bp
    from app.routes.donation import donation_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.notifications import notification_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteers')
    app.register_blueprint(recipient_bp, url_prefix='/recipients')
    app.register_blueprint(donation_bp, url_prefix='/donations')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(notification_bp, url_prefix='/notifications')

    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    
    return app"""
