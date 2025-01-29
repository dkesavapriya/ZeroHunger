from geopy.distance import geodesic

def find_nearby_users(location, radius=10):
    """
    Find nearby users within a given radius (in kilometers).
    """
    from app.models import User  # Import here to avoid circular imports

    all_users = User.query.all()
    nearby_users = []

    for user in all_users:
        user_location = tuple(map(float, user.location.split(",")))
        distance = geodesic(location, user_location).kilometers
        if distance <= radius:
            nearby_users.append(user)

    return nearby_users

    from geopy.distance import geodesic

def calculate_distance(loc1, loc2):
    """
    Calculate distance between two locations using latitude and longitude.
    loc1 and loc2 should be tuples: (latitude, longitude)
    """
    return geodesic(loc1, loc2).km

