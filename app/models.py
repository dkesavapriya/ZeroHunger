from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'volunteer', 'recipient', 'donor'
    address = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)   # Location for notifications
    longitude = db.Column(db.Float, nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)

    donations = db.relationship('Donation', backref='donor', lazy=True)

    def __repr__(self):
        return f"<User {self.name} - {self.role}>"

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_item = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="Available")  # Available, Accepted, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Donation {self.food_item} - {self.status}>"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification to {self.recipient_id}>"
