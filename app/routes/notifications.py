from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
#from app import db
from app.models import Notification

notification_bp = Blueprint("notification", __name__)

# Fetch all unread notifications for the logged-in user
@notification_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.timestamp.desc()).all()
    
    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "timestamp": n.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": n.is_read
        } for n in notifications
    ]), 200

# Mark a specific notification as read
@notification_bp.route("/notifications/read/<int:notification_id>", methods=["POST"])
@jwt_required()
def mark_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
        return jsonify({"message": "Notification marked as read"}), 200
    return jsonify({"message": "Notification not found"}), 404

# Mark all notifications as read
@notification_bp.route("/notifications/read_all", methods=["POST"])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    
    for notification in notifications:
        notification.is_read = True
    db.session.commit()

    return jsonify({"message": "All notifications marked as read"}), 200
