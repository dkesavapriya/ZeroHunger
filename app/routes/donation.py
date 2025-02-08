from flask import Blueprint, request, jsonify
#from app import db, socketio
from app.models import Donation, Notification, User

donation_bp = Blueprint('donation', __name__)

# 🟢 Post a New Donation
@donation_bp.route("/", methods=["POST"])
def post_donation():
    data = request.get_json()
    new_donation = Donation(
        donor_id=data["donor_id"],
        food_item=data["food_item"],
        quantity=data["quantity"],
        location=data["location"]
    )
    db.session.add(new_donation)
    db.session.commit()

    # 🔔 Send Real-Time Notification to Volunteers
    notification = Notification(user_id=None, message="A new donation is available!")
    db.session.add(notification)
    db.session.commit()
    socketio.emit("new_donation", {"message": "A new donation has been posted!"})

    return jsonify({"message": "Donation posted successfully!"}), 201

# 🔵 Fetch Available Donations
@donation_bp.route("/", methods=["GET"])
def get_donations():
    donations = Donation.query.filter_by(status="Available").all()
    return jsonify([
        {
            "id": d.id,
            "food_item": d.food_item,
            "quantity": d.quantity,
            "location": d.location,
            "status": d.status
        } for d in donations
    ])

# 🟡 Accept a Donation
@donation_bp.route("/accept/<int:donation_id>", methods=["PUT"])
def accept_donation(donation_id):
    donation = Donation.query.get(donation_id)
    if not donation or donation.status != "Available":
        return jsonify({"message": "Donation not found or already taken"}), 404

    donation.status = "Accepted"
    db.session.commit()

    # 🔔 Notify Donor & Volunteers
    notification = Notification(user_id=donation.donor_id, message="Your donation has been accepted!")
    db.session.add(notification)
    db.session.commit()
    socketio.emit("donation_status", {"message": "A donation has been accepted!"})

    return jsonify({"message": "Donation accepted!"}), 200

# 🔴 Mark Donation as Completed
@donation_bp.route("/complete/<int:donation_id>", methods=["PUT"])
def complete_donation(donation_id):
    donation = Donation.query.get(donation_id)
    if not donation or donation.status != "Accepted":
        return jsonify({"message": "Donation not found or not accepted yet"}), 404

    donation.status = "Completed"
    db.session.commit()

    # 🔔 Notify Donor
    notification = Notification(user_id=donation.donor_id, message="Your donation has been successfully completed!")
    db.session.add(notification)
    db.session.commit()
    socketio.emit("donation_completed", {"message": "A donation has been completed!"})

    return jsonify({"message": "Donation completed!"}), 200
