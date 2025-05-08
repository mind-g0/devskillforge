import sys
import os

# Ensure the app\'s root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src import create_app, db
from src.models import Challenge, User

app = create_app()

def seed_challenges():
    with app.app_context():
        # Check if admin user exists, create if not
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(username="admin", email="admin@example.com", role="Admin")
            admin_user.set_password("adminpassword") # Set a default password
            db.session.add(admin_user)
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        # Sample Challenges
        challenges_data = [
            {
                "title": "Simple HTML Page",
                "instructions": "Create a basic HTML page with a heading (h1) that says \"Hello, World!\" and a paragraph (p) below it with some lorem ipsum text.",
                "starter_code": "<!DOCTYPE html>\n<html>\n<head>\n    <title>My First Page</title>\n</head>\n<body>\n    <!-- Your code here -->\n</body>\n</html>",
                "language_type": "HTML/CSS/JS",
                "category": "HTML/CSS/JS"
            },
            {
                "title": "CSS Button Styling",
                "instructions": "You are given a simple HTML button. Style it using CSS to have a blue background, white text, padding of 10px 20px, and rounded corners (5px border-radius). Add a hover effect that changes the background to a darker blue.",
                "starter_code": "<!DOCTYPE html>\n<html>\n<head>\n<title>CSS Button</title>\n<style>\n  /* Your CSS here */\n  .myButton {\n    /* Initial styles */\n  }\n  .myButton:hover {\n    /* Hover styles */\n  }\n</style>\n</head>\n<body>\n  <button class=\"myButton\">Click Me</button>\n</body>\n</html>",
                "language_type": "HTML/CSS/JS",
                "category": "HTML/CSS/JS"
            },
            {
                "title": "Python: Sum Two Numbers",
                "instructions": "Write a Python function called `sum_numbers` that takes two arguments (a and b) and returns their sum.",
                "starter_code": "def sum_numbers(a, b):\n    # Your code here\n    pass\n\n# Example (the testing environment will call your function):\n# print(sum_numbers(5, 3))",
                "language_type": "Python",
                "category": "Python"
            },
            {
                "title": "Python: Factorial",
                "instructions": "Write a Python function called `factorial` that takes a non-negative integer `n` and returns its factorial. The factorial of 0 is 1.",
                "starter_code": "def factorial(n):\n    if n < 0:\n        return \"Factorial not defined for negative numbers\"\n    # Your code here\n    pass\n\n# Example:\n# print(factorial(5)) # Expected output: 120",
                "language_type": "Python",
                "category": "Python"
            },
            {
                "title": "SQL: Select All Employees",
                "instructions": "Write a SQL query to select all columns for all records from the `employees` table.",
                "starter_code": "SELECT * FROM employees;",
                "language_type": "SQL",
                "category": "SQL"
            },
            {
                "title": "SQL: Employees in Engineering",
                "instructions": "Write a SQL query to select the `name` and `salary` of all employees who are in the \"Engineering\" department.",
                "starter_code": "SELECT name, salary FROM employees WHERE department = \"Engineering\";",
                "language_type": "SQL",
                "category": "SQL"
            }
        ]

        existing_titles = [c.title for c in Challenge.query.all()]
        added_count = 0
        for data in challenges_data:
            if data['title'] not in existing_titles:
                challenge = Challenge(**data)
                db.session.add(challenge)
                added_count += 1
                print(f"Adding challenge: {data['title']}")
            else:
                print(f"Challenge '{data['title']}' already exists. Skipping.")
        
        if added_count > 0:
            db.session.commit()
            print(f"{added_count} new challenges added successfully.")
        else:
            print("No new challenges were added.")

if __name__ == "__main__":
    seed_challenges()

