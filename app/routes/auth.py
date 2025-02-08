from flask import Blueprint, request, jsonify
#from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# Register a new user
@auth_bp.route("/register", methods=["GET","POST"])
def register():
    data = request.json
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=data["role"],
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login user
'''@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400
        
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "role": user.role}), 200'''

# Get user details
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    print(request.headers)  # Check if Authorization header is received
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return jsonify({
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200

@auth_bp.route("/logout")
@jwt_required()  # Ensure only logged-in users can call this
def logout():
    return jsonify({"message": "Logout successful. Please delete the token on the client-side."}), 200

