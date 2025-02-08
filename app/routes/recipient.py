from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ..models import User

recipient_bp = Blueprint('recipient', __name__)

# Get all recipients
@recipient_bp.route('/recipients', methods=['GET'])
@jwt_required()
def get_recipients():
    recipients = User.query.filter_by(role="recipient").all()
    recipient_list = [{"id": r.id, "name": r.name, "email": r.email, "location": r.location} for r in recipients]
    return jsonify(recipient_list), 200
