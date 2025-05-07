from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from src.models import Challenge
from src import db # For potential submission saving
import requests # For Piston API
import sqlite3 # For SQL execution
import os # For SQLite DB path

challenges_bp = Blueprint("challenges", __name__)

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "sandbox_db", "training.db")

# Helper function to create a dummy training.db if it doesn't exist for SQL challenges
def ensure_training_db():
    db_dir = os.path.dirname(SQLITE_DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if not os.path.exists(SQLITE_DB_PATH):
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        # Create a sample table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER
        );
        """)
        # Insert sample data
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Alice", "Engineering", 70000))
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Bob", "Marketing", 65000))
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", ("Charlie", "Engineering", 72000))
        conn.commit()
        conn.close()

ensure_training_db() # Ensure it exists on app startup

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

        if language == "python":
            try:
                payload = {
                    "language": "python",
                    "version": "3.10.0", # Specify a version, check Piston docs for available versions
                    "files": [{"name": "main.py", "content": code}]
                }
                response = requests.post(PISTON_API_URL, json=payload, timeout=10) # Added timeout
                response_data = response.json()
                if response.status_code == 200:
                    run_info = response_data.get("run", {})
                    output = run_info.get("stdout", "")
                    error_output = run_info.get("stderr", "")
                    if not output and not error_output and run_info.get("code", 0) != 0:
                        error_output = run_info.get("output", "Execution failed, no specific error message.") # Piston sometimes puts combined output here
                    elif not output and not error_output:
                         output = "(No output)"
                else:
                    error_output = f"Error from Piston API: {response_data.get('message', response.text)}"
            except requests.exceptions.RequestException as e:
                error_output = f"Failed to connect to Piston API: {e}"
            except Exception as e:
                error_output = f"An unexpected error occurred during Python execution: {e}"

        elif language in ["html/js", "html/css/js"]:
            output = code # For HTML/JS, the code itself is the output to be rendered in an iframe
        
        elif language == "sql":
            # Ensure the query is read-only (very basic check, more robust parsing/validation needed for production)
            if not code.strip().upper().startswith("SELECT"):
                error_output = "Only SELECT queries are allowed for SQL challenges."
            else:
                try:
                    conn = sqlite3.connect(SQLITE_DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute(code)
                    results = cursor.fetchall()
                    if results:
                        # Format results as a simple string table
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

        if error_output:
            flash(error_output, "danger")
        elif output:
            flash("Code executed! Check output below.", "success")
        else: # No output and no error
            flash("Code executed, but produced no output.", "info")
            
        return render_template("challenge_detail.html", title=challenge.title, challenge=challenge, output=output, error_output=error_output, submitted_code=code)

    return render_template("challenge_detail.html", title=challenge.title, challenge=challenge, submitted_code=submitted_code)


