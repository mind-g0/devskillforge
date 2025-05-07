from flask import Blueprint, render_template
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    return render_template("home.html", title="Home")

