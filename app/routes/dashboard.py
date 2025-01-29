from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Donation, User
from app.utils import calculate_distance

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """
    Provide dashboard data based on user role.
    """
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if user.role == 'Donor':
        # Fetch all donations posted by the user
        donations = Donation.query.filter_by(posted_by_id=user.id).all()
        return render_template('dashboard.html', role='Donor', donations=donations)

    elif user.role in ['Volunteer', 'Recipient']:
        # Fetch nearby donations
        all_donations = Donation.query.filter_by(is_accepted=False).all()
        nearby_donations = [
            donation for donation in all_donations
            if calculate_distance(user.location, donation.location) < 10
        ]
        return render_template('dashboard.html', role=user.role, donations=nearby_donations)

    return jsonify({"error": "Invalid user role"}), 400
