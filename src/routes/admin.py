from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from src import db
from src.models import User, Challenge, UserChallengeSubmission
from src.decorators import admin_required
# Import forms for admin actions later (e.g., ChallengeForm, UserRoleForm)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@admin_required
def admin_dashboard():
    users = User.query.all()
    challenges = Challenge.query.all()
    return render_template("admin/admin_dashboard.html", title="Admin Dashboard", users=users, challenges=challenges)

# Placeholder for Challenge Management
@admin_bp.route("/challenges")
@admin_required
def manage_challenges():
    challenges = Challenge.query.all()
    return render_template("admin/manage_challenges.html", title="Manage Challenges", challenges=challenges)

@admin_bp.route("/challenges/add", methods=["GET", "POST"])
@admin_required
def add_challenge():
    # Add ChallengeForm logic here later
    if request.method == "POST":
        # Process form data
        title = request.form.get("title")
        instructions = request.form.get("instructions")
        starter_code = request.form.get("starter_code")
        language_type = request.form.get("language_type")
        category = request.form.get("category")
        
        if not all([title, instructions, language_type, category]):
            flash("All fields except starter code are required.", "danger")
        else:
            new_challenge = Challenge(title=title, instructions=instructions, starter_code=starter_code, language_type=language_type, category=category)
            db.session.add(new_challenge)
            db.session.commit()
            flash("Challenge added successfully!", "success")
            return redirect(url_for("admin.manage_challenges"))
    return render_template("admin/add_challenge.html", title="Add Challenge")

@admin_bp.route("/challenges/edit/<int:challenge_id>", methods=["GET", "POST"])
@admin_required
def edit_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    # Add ChallengeForm logic here later, pre-filled with challenge data
    if request.method == "POST":
        challenge.title = request.form.get("title", challenge.title)
        challenge.instructions = request.form.get("instructions", challenge.instructions)
        challenge.starter_code = request.form.get("starter_code", challenge.starter_code)
        challenge.language_type = request.form.get("language_type", challenge.language_type)
        challenge.category = request.form.get("category", challenge.category)
        db.session.commit()
        flash("Challenge updated successfully!", "success")
        return redirect(url_for("admin.manage_challenges"))
    return render_template("admin/edit_challenge.html", title="Edit Challenge", challenge=challenge)

@admin_bp.route("/challenges/delete/<int:challenge_id>", methods=["POST"])
@admin_required
def delete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    # Consider implications: what happens to user submissions for this challenge?
    # For now, simple delete.
    db.session.delete(challenge)
    db.session.commit()
    flash("Challenge deleted successfully!", "success")
    return redirect(url_for("admin.manage_challenges"))

# Placeholder for User Management
@admin_bp.route("/users")
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", title="Manage Users", users=users)

@admin_bp.route("/users/edit_role/<int:user_id>", methods=["POST"])
@admin_required
def edit_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")
    if new_role in ["Student", "Admin"]:
        user.role = new_role
        db.session.commit()
        flash(f"User {user.username}\\'s role updated to {new_role}.", "success")
    else:
        flash("Invalid role specified.", "danger")
    return redirect(url_for("admin.manage_users"))


