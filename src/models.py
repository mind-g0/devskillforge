from src import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="Student") # Roles: Student, Admin

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(\'{self.username}\", \'{self.email}\", \'{self.role}\')"




class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=True)
    language_type = db.Column(db.String(20), nullable=False)  # HTML/JS, Python, SQL
    category = db.Column(db.String(50), nullable=False) # HTML/CSS/JS, Python, SQL, APIs, Full Stack

    def __repr__(self):
        return f"Challenge(\\'{self.title}\\', \\'{self.language_type}\\', \\'{self.category}\\')"

