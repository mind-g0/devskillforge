from src import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="Student") # Roles: Student, Admin
    submissions = db.relationship("UserChallengeSubmission", backref="submitter", lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(\"{self.username}\", \"{self.email}\", \"{self.role}\")"

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=True)
    language_type = db.Column(db.String(20), nullable=False)  # HTML/JS, Python, SQL
    category = db.Column(db.String(50), nullable=False) # HTML/CSS/JS, Python, SQL, APIs, Full Stack
    submissions = db.relationship("UserChallengeSubmission", backref="challenge_info", lazy=True)

    def __repr__(self):
        return f"Challenge(\"{self.title}\", \"{self.language_type}\", \"{self.category}\")"

class UserChallengeSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"), nullable=False)
    submitted_code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    output = db.Column(db.Text, nullable=True)
    error_output = db.Column(db.Text, nullable=True)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_correct = db.Column(db.Boolean, nullable=True) # Optional: for future auto-grading

    def __repr__(self):
        return f"Submission(user_id={self.user_id}, challenge_id={self.challenge_id}, date=\"{self.submission_date}\")"

