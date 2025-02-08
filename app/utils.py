from geopy.distance import geodesic
from app.models import User
from app import db

def find_nearby_users(location, radius=10):
    """
    Find nearby users within a given radius (in kilometers).
    """
    nearby_users = []

    # Fetch users from the database and calculate the distance
    all_users = User.query.all()
    
    for user in all_users:
        try:
            # Assume user.location is a string like "lat,lng"
            user_location = tuple(map(float, user.location.split(",")))
            distance = geodesic(location, user_location).kilometers
            if distance <= radius:
                nearby_users.append(user)
        except ValueError:
            continue  # Skip user if location is invalid or not formatted correctly

    return nearby_users


def calculate_distance(loc1, loc2):
    """
    Calculate distance between two locations using latitude and longitude.
    loc1 and loc2 should be tuples: (latitude, longitude)
    """
    return geodesic(loc1, loc2).km


def send_notification(users, message):
    """
    Send notifications to a list of users.
    """
    for user in users:
        notification = Notification(user_id=user.id, message=message)
        db.session.add(notification)
    
    db.session.commit()

