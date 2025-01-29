import threading
import time
from flask_socketio import SocketIO
from app.models import User, Donation
from app.utils import calculate_distance
from flask import current_app

# Initialize SocketIO (if not already in `app/__init__.py`)
socketio = SocketIO(cors_allowed_origins="*")

def notify_nearby_users(donation):
    """
    Notify nearby users (volunteers and recipients) about a new donation.
    """
    users = User.query.filter(User.role.in_(["Volunteer", "Recipient"])).all()
    nearby_users = [
        user for user in users if calculate_distance(donation.location, user.location) < 10  # Within 10 km radius
    ]

    for user in nearby_users:
        socketio.emit(
            "new_donation",
            {"message": f"New donation posted: {donation.title} at {donation.location}"},
            room=str(user.id),
        )

    # Start a background thread for fallback notifications
    thread = threading.Thread(target=send_fallback_notifications, args=(donation, nearby_users))
    thread.daemon = True
    thread.start()

def notify_donor_acceptance(donation, user):
    """
    Notify the donor when their donation is accepted.
    """
    socketio.emit(
        "donation_accepted",
        {"message": f"Your donation '{donation.title}' has been accepted by {user.name}."},
        room=str(donation.posted_by_id),
    )

def send_fallback_notifications(donation, initial_users):
    """
    Notify the next set of users if the donation is not accepted within a time frame.
    """
    time.sleep(60)  # Wait for 60 seconds before fallback notifications

    with current_app.app_context():  # Ensure the database query runs within Flask's app context
        donation = Donation.query.get(donation.id)

        if not donation.is_accepted:
            # Get all users excluding the initial notified users
            all_users = User.query.filter(User.role.in_(["Volunteer", "Recipient"])).all()
            next_users = [
                user for user in all_users
                if user.id not in [u.id for u in initial_users] and
                calculate_distance(donation.location, user.location) < 20  # 20 km radius
            ]

            for user in next_users:
                socketio.emit(
                    "new_donation",
                    {"message": f"Fallback notification: {donation.title} at {donation.location}"},
                    room=str(user.id),
                )
