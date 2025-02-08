from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ..models import User

volunteer_bp = Blueprint('volunteer', __name__)

# Get all volunteers
@volunteer_bp.route('/volunteers', methods=['GET'])
@jwt_required()
def get_volunteers():
    volunteers = User.query.filter_by(role="volunteer").all()
    volunteer_list = [{"id": v.id, "name": v.name, "email": v.email, "location": v.location} for v in volunteers]
    return jsonify(volunteer_list), 200
