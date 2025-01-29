from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Donation
from app import db

recipient_bp = Blueprint("recipient", __name__)

@recipient_bp.route("/donations", methods=["GET"])
@jwt_required()
def view_donations():
    """
    View all donations available for recipients.
    """
    current_user = get_jwt_identity()
    if current_user["role"] != "Recipient":
        return jsonify({"error": "Access denied"}), 403

    # Query all donations from the database
    donations = Donation.query.filter_by(status="available").all()

    donation_list = [
        {
            "id": donation.id,
            "title": donation.title,
            "description": donation.description,
            "location": donation.location,
            "posted_by": donation.posted_by.name,
        }
        for donation in donations
    ]

    return jsonify({"donations": donation_list}), 200


@recipient_bp.route("/accept_donation/<int:donation_id>", methods=["POST"])
@jwt_required()
def accept_donation(donation_id):
    """
    Accept a donation.
    """
    current_user = get_jwt_identity()
    if current_user["role"] != "Recipient":
        return jsonify({"error": "Access denied"}), 403

    # Find the donation
    donation = Donation.query.get(donation_id)
    if not donation or donation.status != "available":
        return jsonify({"error": "Donation not available"}), 404

    # Update donation status
    donation.status = "accepted"
    donation.accepted_by = current_user["id"]  # Assign the recipient
    db.session.commit()

    return jsonify({"message": "Donation accepted successfully!"}), 200
