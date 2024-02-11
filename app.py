from enum import Enum
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking
db = SQLAlchemy(app)

# User roles (enum type for clarity and security)
class Role(Enum):
    EMPLOYEE = 1
    ADMIN = 2

# User model with role and password hashing
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Login manager and session handling
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page on unauthorized access

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@login_required
def home():
    # Implement welcome message, news, announcements, etc.
    return render_template('home.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Add routes for different employee functionalities based on roles
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def employee_dashboard():
    # Implement functionalities relevant to employees, e.g., leave requests, pay information, etc.
    return render_template('employee_dashboard.html', user=current_user)

@app.route('/leave', methods=['GET', 'POST'])
@login_required
def employee_leave():
    # Implement leave application, history, cancellation, etc.
    return render_template('employee_leave.html', user=current_user)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist (ideally with separate commands)
        db.create_all()

        # Create an initial admin user (temporary, replace with proper registration flow)
        admin = User(username='admin', password='password123', role=Role.ADMIN)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True)
