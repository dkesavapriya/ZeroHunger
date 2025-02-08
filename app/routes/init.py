from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

init_bp = Blueprint('init_bp', __name__)

@init_bp.route('/')
def index():
    return render_template('index.html')  # This renders the main landing page (e.g., dashboard or login)
