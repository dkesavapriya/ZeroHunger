from flask import Blueprint, request, jsonify
from app.models import User, Donation
from app.notifications import notify_nearby_users
from flask_jwt_extended import jwt_required
from app import db

donation_bp = Blueprint("donation", __name__)

@donation_bp.route("/post", methods=["POST"])
def post_donation():
    """
    Endpoint to post a new donation.
    """
    data = request.get_json()
    item = data.get("item")
    donor_id = data.get("donor_id")

    # Validate data
    if not item or not donor_id:
        return jsonify({"error": "Item and donor ID are required"}), 400

    # Create donation entry
    donation = Donation(item=item, donor_id=donor_id)
    db.session.add(donation)
    db.session.commit()

    # Send notifications to nearby volunteers and recipients
    donor = User.query.get(donor_id)
    if donor:
        nearby_users = find_nearby_users(donor.location)  # Custom function
        send_notification(nearby_users, f"New donation posted: {item}")

    return jsonify({"message": "Donation posted successfully!"}), 201


@donation_bp.route("/accept/<int:donation_id>", methods=["POST"])
@jwt_required()
def accept_donation(donation_id):
    """
    Accept a donation and notify the donor.
    """
    current_user = get_jwt_identity()
    donation = Donation.query.get(donation_id)

    if not donation:
        return jsonify({"error": "Donation not found."}), 404

    if donation.is_accepted:
        return jsonify({"error": "Donation already accepted."}), 400

    # Update donation status
    donation.is_accepted = True
    donation.accepted_by_id = current_user["id"]
    db.session.commit()

    # Notify donor
    notify_donor_acceptance(donation, current_user)

    return jsonify({"message": "Donation accepted successfully!"}), 200

@donation_bp.route("/", methods=["GET"])
def get_all_donations():
    """
    Endpoint to get all donation posts.
    """
    donations = Donation.query.all()
    result = [
        {
            "id": d.id,
            "item": d.item,
            "status": d.status,
            "donor": d.donor.name,
            "recipient": d.recipient.name if d.recipient else None,
        }
        for d in donations
    ]
    return jsonify(result), 200
@donation_bp.route("/create", methods=["POST"])
@jwt_required()
def create_donation():
    """
    Create a new donation post and notify nearby users.
    """
    data = request.get_json()
    current_user = get_jwt_identity()

    if current_user["role"] != "Donor":
        return jsonify({"error": "Only donors can create donations."}), 403

    donation = Donation(
        title=data["title"],
        description=data["description"],
        location=data["location"],
        posted_by_id=current_user["id"],
    )
    db.session.add(donation)
    db.session.commit()

    # Notify nearby users
    notify_nearby_users(donation)

    return jsonify({"message": "Donation posted successfully!"}), 201
