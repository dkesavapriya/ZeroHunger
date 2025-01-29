from flask import Blueprint, request, jsonify
from app.models import User
from app import db

volunteer_bp = Blueprint("volunteer", __name__)

@volunteer_bp.route("/register", methods=["POST"])
def register_volunteer():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    location = data["location"]

    volunteer = User(name=name, email=email, password=password, role="volunteer", location=location)
    db.session.add(volunteer)
    db.session.commit()

    return jsonify({"message": "Volunteer registered successfully!"}), 201
