# DevSkillForge Feature Implementation Plan

## Phase 1: Core Feature Implementation & Enhancement

### 1. User System Enhancements
- [X] User registration, login, logout (Exists)
- [X] User roles: Student, Admin (Exists in model, ensure fully integrated in logic where needed for admin panel access)
- [X] Password hashing, session management (Flask-Login) (Exists)
- [/] User dashboard with progress stats (Basic placeholder exists, needs enhancement for actual stats from completed challenges).

### 2. Challenge Engine
- [X] Challenge Model (Title, Instructions, Starter Code, Language Type, Category) (Exists in `models.py`)
- [X] Backend logic for listing challenges (`/challenges` route) (Exists in `challenges.py`)
- [X] Backend logic for viewing a single challenge (`/challenge/<id>` route) (Exists in `challenges.py`)
- [X] Backend logic for Python code execution via Piston API (Exists in `challenges.py`)
- [X] Backend logic for HTML/CSS/JS code execution (returns code for iframe) (Exists in `challenges.py`)
- [X] Backend logic for SQL code execution against a sandbox SQLite DB (Exists in `challenges.py`, `ensure_training_db()` helper creates sandbox DB)
- [ ] **UI/UX for Challenges:**
    - [ ] Update `/challenges` template (`challenges.html`) to list challenges from the database effectively.
    - [ ] Implement Challenge Categories display/filtering on `challenges.html` (Optional enhancement, basic listing first).
    - [ ] Create/Update `challenge_detail.html` template:
        - [ ] Integrate Code Editor (e.g., Ace Editor) for `starter_code` and user input.
        - [ ] Ensure editor content is submitted with the form.
        - [ ] Clearly display `output` and `error_output` from code execution.
        - [ ] For HTML/CSS/JS challenges, render the `output` (which is the submitted code) in a sandboxed `<iframe>`.
- [ ] **User Submissions & Progress:**
    - [ ] Implement saving of user solutions/submissions (e.g., a `UserChallengeSubmission` model: user_id, challenge_id, submitted_code, language, output, error, submission_date, is_correct (optional)).
    - [ ] Modify `view_challenge` POST logic to save submission.

### 3. Live Code Execution (Backend logic largely exists, UI/UX is key)
- [X] Frontend (HTML/CSS/JS) Execution: Backend returns code. (Needs iframe rendering in `challenge_detail.html`)
- [X] Backend (Python) Execution: Piston API integration exists. (Needs output display in `challenge_detail.html`)
- [X] SQL Training Execution: SQLite execution exists. (Needs output display in `challenge_detail.html`)

### 4. User Dashboard Enhancements
- [ ] Fetch and display actual completed challenges for users (requires `UserChallengeSubmission` model and logic).
- [ ] Implement basic Points & XP system based on completed challenges.
- [ ] Implement "Revisit Past Submissions" (requires `UserChallengeSubmission` model and a new route/template).
- [ ] Placeholder for Badges, Weekly Goals & Streaks (mark as "Coming Soon" if not fully implemented).

### 5. Admin Panel (Core Functionality)
- [ ] Create admin-only routes/decorators (e.g., check `current_user.role == 'Admin'` or a dedicated `admin_required` decorator).
- [ ] **Challenge Management (Admin):**
    - [ ] Create templates for Admin: `admin_dashboard.html`, `admin_challenge_form.html`, `admin_challenge_list.html`.
    - [ ] Implement routes and forms for Admins to Add new Challenges.
    - [ ] Implement routes and forms for Admins to Edit existing Challenges.
    - [ ] Implement logic for Admins to Delete Challenges.
- [ ] **User Management (Admin - Basic):**
    - [ ] Implement UI for Admins to View Users.
    - [ ] Implement UI for Admins to Manage User Roles (e.g., promote a user to Admin).
- [ ] Placeholder for Admin view of user progress/submissions (mark as "Coming Soon" if not fully implemented).
- [ ] Placeholder for Admin content moderation (mark as "Coming Soon" if not fully implemented).

## Phase 2: Seeding Content

- [ ] **Seed Sample Challenges (Application DB, not just SQL sandbox):**
    - [ ] Create a script or a one-time route (admin-protected) to add sample challenges to the `Challenge` table.
    - [ ] Add 1-2 HTML/CSS/JS sample challenges.
    - [ ] Add 1-2 Python sample challenges.
    - [ ] Add 1-2 SQL sample challenges (these will use the `training.db` for their execution environment).

## Phase 3: Optional Features & Refinements

### 6. Learning Hub (Optional - If time permits)
- [ ] Basic Blog section with Markdown-rendered tutorials.
- [ ] Categorization by topic.

## Phase 4: Validation, Documentation & Deployment Prep

- [ ] Validate all newly implemented features and seeded challenges.
- [ ] **Create Comprehensive Documentation:**
    - [ ] Document how the platform works (overall architecture, user flow, admin flow).
    - [ ] Document how to add new challenges in the future (for admins).
    - [ ] Document setup and deployment steps (especially for PythonAnywhere).
    - [ ] Save documentation as Markdown files (e.g., `PLATFORM_DOCS.md`, `ADMIN_GUIDE.md`).
- [ ] Update `requirements.txt` if new dependencies were added.
- [ ] Ensure project structure and practices align with PythonAnywhere deployment (e.g., WSGI setup, environment variables).
- [ ] Report completion and provide updated project (including docs) to user.
