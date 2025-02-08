from flask import Blueprint, jsonify,render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Donation, db

# Create the Blueprint for dashboard
dashboard_bp = Blueprint("dashboard", __name__ ,url_prefix="/dashboard")



# Endpoint to fetch dashboard stats (total donations, accepted, pending, user donations)
@dashboard_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get stats
    total_donations = Donation.query.count()
    accepted_donations = Donation.query.filter(Donation.accepted_by.isnot(None)).count()
    pending_donations = total_donations - accepted_donations
    user_donations = Donation.query.filter_by(donor_id=user_id).count()
    user_accepted = Donation.query.filter_by(accepted_by_id=user_id).count()

    return jsonify({
        "total_donations": total_donations,
        "accepted_donations": accepted_donations,
        "pending_donations": pending_donations,
        "user_donations": user_donations,
        "user_accepted": user_accepted
    })

# Fetch all available donations (only pending donations)
@dashboard_bp.route("/donations", methods=["GET"])
@jwt_required()
def get_donations():
    donations = Donation.query.filter_by(status="Pending").all()
    return jsonify([{
        "id": d.id,
        "food_item": d.food_item,
        "quantity": d.quantity,
        "status": d.status
    } for d in donations]), 200

# Accept a donation (for volunteers or recipients only)
@dashboard_bp.route("/donations/accept/<int:donation_id>", methods=["POST"])
@jwt_required()
def accept_donation(donation_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Check if user has the correct role to accept donations
    if user.role not in ["volunteer", "recipient"]:
        return jsonify({"error": "Only volunteers or recipients can accept donations"}), 403

    # Get the donation and ensure it's in the "Pending" status
    donation = Donation.query.get(donation_id)
    if not donation or donation.status != "Pending":
        return jsonify({"error": "Invalid donation"}), 400

    # Accept the donation
    donation.status = "Accepted"
    donation.accepted_by = user_id
    db.session.commit()

    return jsonify({"message": "Donation accepted successfully"}), 200
