from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    """
    Model representing an employee in the portal.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Add more attributes as needed, like department, role, etc.

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}>"

# Add other models here, for example:
# class Department(db.Model):
#     ...
# class LeaveRequest(db.Model):
#     ...

db.create_all()  # Create tables if they don't exist (modify if needed)
