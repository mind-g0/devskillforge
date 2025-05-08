from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from src.models import Challenge, UserChallengeSubmission # Added UserChallengeSubmission
from src import db
import requests # For Piston API
import sqlite3 # For SQL execution
import os # For SQLite DB path

challenges_bp = Blueprint("challenges", __name__)

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"
# Ensure the sandbox_db directory is at the root of the project, next to src
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sandbox_db", "training.db")


def ensure_training_db():
    db_dir = os.path.dirname(SQLITE_DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if not os.path.exists(SQLITE_DB_PATH):
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER
        );
        """)
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Alice", "Engineering", 70000))
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Bob", "Marketing", 65000))
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Charlie", "Engineering", 72000))
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL
        );
        """)
        cursor.execute("INSERT INTO products (product_name, category, price) VALUES (?, ?, ?)", ("Laptop", "Electronics", 1200.00))
        cursor.execute("INSERT INTO products (product_name, category, price) VALUES (?, ?, ?)", ("Keyboard", "Electronics", 75.00))
        cursor.execute("INSERT INTO products (product_name, category, price) VALUES (?, ?, ?)", ("Desk Chair", "Furniture", 150.00))
        conn.commit()
        conn.close()

ensure_training_db()

@challenges_bp.route("/challenges")
@login_required
def list_challenges():
    challenges = Challenge.query.all()
    return render_template("challenges.html", title="Challenges", challenges=challenges)

@challenges_bp.route("/challenge/<int:challenge_id>", methods=["GET", "POST"])
@login_required
def view_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    output = None
    error_output = None
    submitted_code = request.form.get("code") if request.method == "POST" else challenge.starter_code

    if request.method == "POST":
        code = request.form.get("code")
        language = challenge.language_type.lower()
        is_correct_submission = False # Placeholder for actual correctness check

        if language == "python":
            try:
                payload = {
                    "language": "python",
                    "version": "3.10.0",
                    "files": [{"name": "main.py", "content": code}]
                }
                response = requests.post(PISTON_API_URL, json=payload, timeout=10)
                response_data = response.json()
                if response.status_code == 200:
                    run_info = response_data.get("run", {})
                    output = run_info.get("stdout", "")
                    error_output = run_info.get("stderr", "")
                    if not output and not error_output and run_info.get("code", 0) != 0:
                        error_output = run_info.get("output", "Execution failed, no specific error message.")
                    elif not output and not error_output:
                         output = "(No output)"
                else:
                    message = response_data.get("message", response.text)
                    error_output = f"Error from Piston API: {message}"
            except requests.exceptions.RequestException as e:
                error_output = f"Failed to connect to Piston API: {e}"
            except Exception as e:
                error_output = f"An unexpected error occurred during Python execution: {e}"

        elif language in ["html/js", "html/css/js"]:
            output = code
        
        elif language == "sql":
            if not code.strip().upper().startswith("SELECT"):
                error_output = "Only SELECT queries are allowed for SQL challenges."
            else:
                try:
                    conn = sqlite3.connect(SQLITE_DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute(code)
                    results = cursor.fetchall()
                    if results:
                        headers = [description[0] for description in cursor.description]
                        output = " | ".join(headers) + "\n"
                        output += "-" * (len(output) -1) + "\n"
                        for row in results:
                            output += " | ".join(map(str, row)) + "\n"
                    else:
                        output = "Query executed successfully, no results to display." if cursor.description else "Query executed successfully (e.g., DDL, no results)."
                    conn.close()
                except sqlite3.Error as e:
                    error_output = f"SQL Error: {e}"
                except Exception as e:
                    error_output = f"An unexpected error occurred during SQL execution: {e}"
        else:
            error_output = "Unsupported language type for execution."

        # Save submission
        submission = UserChallengeSubmission(
            user_id=current_user.id,
            challenge_id=challenge.id,
            submitted_code=code,
            language=language,
            output=output,
            error_output=error_output,
            is_correct=is_correct_submission # Update this if you implement correctness checking
        )
        db.session.add(submission)
        db.session.commit()

        if error_output:
            flash(error_output, "danger")
        elif output:
            flash("Code executed! Check output below. Submission saved.", "success")
        else:
            flash("Code executed, but produced no output. Submission saved.", "info")
            
        return render_template("challenge_detail.html", title=challenge.title, challenge=challenge, output=output, error_output=error_output, submitted_code=code)

    return render_template("challenge_detail.html", title=challenge.title, challenge=challenge, submitted_code=submitted_code)

@challenges_bp.route("/submissions")
@login_required
def list_submissions():
    user_submissions = UserChallengeSubmission.query.filter_by(user_id=current_user.id).order_by(UserChallengeSubmission.submission_date.desc()).all()
    return render_template("submissions.html", title="My Submissions", submissions=user_submissions)

