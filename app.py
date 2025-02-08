from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity,create_access_token
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app.config import Config
from app.models import User,db
# Initialize Flask extensions
#db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="http://127.0.0.1:5000")






def create_app():
    app = Flask(__name__,template_folder="templates")
    app.config.from_object(Config)
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    #from app.models import User

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.volunteer import volunteer_bp
    from app.routes.recipient import recipient_bp
    from app.routes.donation import donation_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.notifications import notification_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteers')
    app.register_blueprint(recipient_bp, url_prefix='/recipients')
    app.register_blueprint(donation_bp, url_prefix='/donations')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(notification_bp, url_prefix='/notifications')

    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    
    return app
app = create_app()


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        address = request.form.get('address', None)  # Handle optional fields
        latitude = request.form.get('latitude', None)
        longitude = request.form.get('longitude', None)
        contact_number = request.form.get('contact_number', None)
            
            
        #from app.models import User
            # Check if user already exists
        #with app.app_context():  # ✅ Ensure app context before querying
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!', 'danger')
            return redirect(url_for('register'))

                # Hash password and create new user
        hashed_password = generate_password_hash(password)
        print("Hashed Password:", hashed_password)
        new_user = User(name=name, email=email, role=role, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("Session Data:", session) 

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

        
#@app.route('/auth/login',methods=["GET","POST"])
#def login():
    ''' if request.method == "POST":
        email = request.get("email")
        password = request.get("password")
    
        
        user = User.query.filter_by(email=email).first()
        if user:
            print("User found:", user.email)  # Debugging
        else:
            print("User not found")
        if user and check_password_hash(user.password, password):  # ✅ Correct password check
  # Verify password
            session["user_id"] = user.id  # Store user ID in session
            print("Login successful for:", user.email)
            print("User logged in, session set:", session)  # Debugging
            return redirect(url_for("dashboard"))
        else:
            print("Invalid login attempt for email:", email)
            flash("Invalid credentials", "danger")
    
    return render_template("login.html")'''
    ''' data = request.get_json()  # Read JSON data
    email = data.get("email")
    password = data.get("password")

    print("Received email:", email)  # Debugging
    print("Received password:", password)  # Debugging

    if not email or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        print("User found:", user.email)  # Debugging
    else:
        print("User not found")
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        print("Invalid password for:", email)
        return jsonify({"success": False, "message": "Invalid credentials"}), 401'''
from werkzeug.security import check_password_hash

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")  # Show login page

    # Handle POST login request
    #print("Request Headers:", request.headers)
    #print("Content-Type:", request.content_type)
    #print("Request Data:", request.data)

    if request.content_type == "application/json":
        data = request.get_json()
        print("Received JSON Data:", data)
    else:
        data = request.form
        print("Received Form Data:", data)

    email = data.get("email")
    password = data.get("password")
    
    print("Extracted Email:", email)
    print("Extracted Password:", password)

    if not email or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.id) 
        session["user_id"] = user.id
        return jsonify({"token": token, "redirect": "/dashboard"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/dashboard")
def dashboard():
    print("Session Data:", session)  # Debugging statement
    
    if "user_id" not in session:
        print("User not in session, redirecting to login...")
        return redirect(url_for("login"))  # ✅ Fix redirect issue
  # Redirect if session not found
    
    user = User.query.get(session["user_id"])  # Fetch user from DB
    if not user:
        print("User not found in database, redirecting to login...")
        return redirect(url_for("login"))  # ✅ Fix redirect issue
 # Redirect if user is not in DB
    
    return render_template("dashboard.html", user=user)


@app.route('/donation')
def donation():
    return render_template('donation.html')




if __name__ == '__main__':
   # with app.app_context():
     #   db.create_all()
    socketio.run(app, debug=True)

