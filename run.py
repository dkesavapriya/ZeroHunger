from app import create_app, db, socketio
from app.routes.dashboard import dashboard_bp

# Register the dashboard blueprint
#app.register_blueprint(dashboard_bp)


app = create_app()
#app.register_blueprint(dashboard_bp)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
