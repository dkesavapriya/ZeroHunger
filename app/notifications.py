from flask_socketio import SocketIO, emit
from flask import request
from app import socketio
from app.models import User, Donation
from geopy.distance import geodesic

# Store connected users for real-time notifications
connected_users = {}

@socketio.on("connect")
def handle_connect():
    """Handles new user connections."""
    user_id = request.args.get("user_id")  # Expect user_id to be passed on connection
    if user_id:
        connected_users[user_id] = request.sid
    print(f"User {user_id} connected with session ID {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    """Handles user disconnections."""
    for user_id, sid in connected_users.items():
        if sid == request.sid:
            del connected_users[user_id]
            break
    print(f"User disconnected: {request.sid}")

def send_notification(user_id, message):
    """Send a notification to a specific user if they are connected."""
    sid = connected_users.get(str(user_id))  # Convert user_id to string for dictionary lookup
    if sid:
        emit("notification", {"message": message}, room=sid)

# Notify nearby volunteers & recipients when a new donation is posted
def notify_new_donation(donation):
    all_users = User.query.filter(User.role.in_(["volunteer", "recipient"])).all()
    
    for user in all_users:
        if user.latitude and user.longitude:
            distance = geodesic((donation.latitude, donation.longitude), (user.latitude, user.longitude)).km
            if distance <= 10:  # Only notify users within a 10 km radius
                send_notification(user.id, f"New donation available near you: {donation.item_name}")

# Notify donor when their donation is accepted
def notify_donor(donation):
    donor = User.query.get(donation.donor_id)
    if donor:
        send_notification(donor.id, f"Your donation '{donation.item_name}' was accepted!")

# Notify donor when their donation is completed
def notify_donation_completed(donation):
    donor = User.query.get(donation.donor_id)
    if donor:
        send_notification(donor.id, f"Your donation '{donation.item_name}' has been completed!")
