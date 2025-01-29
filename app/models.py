from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)

class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="available")  # available, accepted, etc.
    posted_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posted_by = db.relationship("User", foreign_keys=[posted_by_id])
    accepted_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    accepted_by = db.relationship("User", foreign_keys=[accepted_by_id])
    is_accepted = db.Column(db.Boolean, default=False)  # New field
    #accepted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # New field
'''class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=True)'''