from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from src.models import Challenge, User
from src import db
from src.forms import ChallengeForm # Using the new ChallengeForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "Admin":
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_required
def admin_dashboard():
    return render_template("admin/dashboard.html", title="Admin Dashboard")

# Challenge Management
@admin_bp.route("/challenges")
@admin_required
def manage_challenges():
    challenges = Challenge.query.all()
    return render_template("admin/manage_challenges.html", title="Manage Challenges", challenges=challenges)

@admin_bp.route("/challenge/add", methods=["GET", "POST"])
@admin_required
def add_challenge():
    form = ChallengeForm()
    if form.validate_on_submit():
        challenge = Challenge(
            title=form.title.data,
            instructions=form.instructions.data,
            starter_code=form.starter_code.data,
            language_type=form.language_type.data,
            category=form.category.data
        )
        db.session.add(challenge)
        db.session.commit()
        flash("Challenge added successfully!", "success")
        return redirect(url_for("admin.manage_challenges"))
    return render_template("admin/add_edit_challenge.html", title="Add Challenge", form=form, legend="New Challenge")

@admin_bp.route("/challenge/edit/<int:challenge_id>", methods=["GET", "POST"])
@admin_required
def edit_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    form = ChallengeForm(obj=challenge)
    if form.validate_on_submit():
        challenge.title = form.title.data
        challenge.instructions = form.instructions.data
        challenge.starter_code = form.starter_code.data
        challenge.language_type = form.language_type.data
        challenge.category = form.category.data
        db.session.commit()
        flash("Challenge updated successfully!", "success")
        return redirect(url_for("admin.manage_challenges"))
    return render_template("admin/add_edit_challenge.html", title="Edit Challenge", form=form, legend=f"Edit Challenge: {challenge.title}")

@admin_bp.route("/challenge/delete/<int:challenge_id>", methods=["POST"])
@admin_required
def delete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    db.session.delete(challenge)
    db.session.commit()
    flash("Challenge deleted successfully!", "success")
    return redirect(url_for("admin.manage_challenges"))

# User Management
@admin_bp.route("/users")
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", title="Manage Users", users=users)

@admin_bp.route("/user/edit_role/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        new_role = request.form.get("role")
        if new_role in ["Student", "Admin"]:
            if user.id == current_user.id and new_role != "Admin":
                 flash("Admins cannot demote themselves.", "danger")
            else:
                user.role = new_role
                db.session.commit()
                flash(f"User {user.username}\\'s role updated to {new_role}.", "success")
        else:
            flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.manage_users"))
    return render_template("admin/edit_user_role.html", title=f"Edit Role for {user.username}", user_to_edit=user)


