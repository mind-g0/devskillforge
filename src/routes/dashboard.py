from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def user_dashboard():
    # Placeholder for actual dashboard data
    progress_stats = {
        "completed_challenges": 0,
        "points": 0,
        "xp": 0,
        "badges": []
    }
    return render_template("dashboard.html", title="Dashboard", stats=progress_stats)

