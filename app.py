from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)
DB = "edupath.db"

# Demo login accounts
USERS = {
    "student1": "student",
    "staff1": "staff",
    "parent1": "parent"
}

# Demo workshop details
WORKSHOPS = [
    {
        "name": "Python Programming",
        "date": "20-11-2026",
        "mode": "Online"
    },
    {
        "name": "Artificial Intelligence",
        "date": "25-11-2026",
        "mode": "Offline"
    },
    {
        "name": "Ethical Hacking",
        "date": "05-12-2026",
        "mode": "Online"
    },
    {
        "name": "Web Development",
        "date": "10-12-2026",
        "mode": "Offline"
    }
]

# Demo scholarship details
SCHOLARSHIPS = [
    {
        "name": "Merit-Based Scholarship",
        "eligibility": "Good academic performance",
        "deadline": "Check official notification"
    },
    {
        "name": "Government Scholarship",
        "eligibility": "As per scheme rules",
        "deadline": "Check official notification"
    },
    {
        "name": "First Graduate Scholarship",
        "eligibility": "Eligible first-generation graduates",
        "deadline": "Check official notification"
    },
    {
        "name": "Need-Based Scholarship",
        "eligibility": "Students meeting financial criteria",
        "deadline": "Check official notification"
    }
]

# Simple demo data
registrations = []
applications = []

STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
    background: #eef3f8;
    margin: 0;
    padding: 20px;
}
.container {
    max-width: 900px;
    margin: 25px auto;
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #ccc;
}
h1 { color: #173b70; }
h2 { color: #176b87; }
.card {
    background: #f8fbff;
    border: 1px solid #d5e2f0;
    padding: 18px;
    margin: 15px 0;
    border-radius: 10px;
}
input, select {
    padding: 10px;
    margin: 8px 0;
    width: 90%;
    max-width: 350px;
    display: block;
}
button, .button {
    background: #176b87;
    color: white;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    text-decoration: none;
    display: inline-block;
    margin: 5px;
    cursor: pointer;
}
.note { color: #555; font-size: 14px; }
</style>
"""

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            username TEXT PRIMARY KEY,
            marks INTEGER DEFAULT 0,
            attendance INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0
        )
    """)
    con.execute("""
        INSERT OR IGNORE INTO students (username)
        VALUES ('student1')
    """)
    con.commit()
    con.close()


def get_student(username="student1"):
    init_db()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    student = con.execute(
        "SELECT * FROM students WHERE username=?",
        (username,)
    ).fetchone()
    con.close()
    return student


def update_student(username, marks, attendance, points):
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT OR IGNORE INTO students (username) VALUES (?)",
        (username,)
    )
    con.execute("""
        UPDATE students
        SET marks=?, attendance=?, points=?
        WHERE username=?
    """, (marks, attendance, points, username))
    con.commit()
    con.close()


def render_page(title, content):
    return render_template_string("""
        {{ style|safe }}
        <div class="container">
            {{ content|safe }}
        </div>
    """, style=STYLE, content=content)


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        role = request.form.get("role", "")

        if USERS.get(username) == role:
            return redirect(url_for(role + "_dashboard"))

        return render_page("Login", """
            <h1>Login Failed</h1>
            <p>Username and role check pannunga.</p>
            <a class="button" href="/">Try Again</a>
        """)

    return render_template_string("""
        {{ style|safe }}
        <div class="container">
            <h1>🎓 EduPath AI</h1>
            <h2>Login Page</h2>

            <form method="post">
                <label>Username</label>
                <input name="username"
                       placeholder="Enter username" required>

                <label>Select Role</label>
                <select name="role">
                    <option value="student">Student</option>
                    <option value="staff">Staff</option>
                    <option value="parent">Parent</option>
                </select>

                <button type="submit">Login</button>
            </form>

            <div class="card">
                <h3>Demo Accounts</h3>
                <p>Student: student1</p>
                <p>Staff: staff1</p>
                <p>Parent: parent1</p>
                <p class="note">
                    Project demo login. Password is not required.
                </p>
            </div>
        </div>
    """, style=STYLE)


# ---------------- STUDENT DASHBOARD ----------------

@app.route("/student")
def student_dashboard():
    student = get_student()

    content = f"""
        <h1>🎓 Student Dashboard</h1>

        <div class="card">
            <h2>📊 Student Progress</h2>
            <p>Username: {student['username']}</p>
            <p>Marks: {student['marks']}</p>
            <p>Attendance: {student['attendance']}%</p>
            <p>Points: {student['points']}</p>
        </div>

        <div class="card">
            <h2>💻 Workshops</h2>
            <p>Explore technical workshops.</p>
            <a class="button" href="/workshops">View Workshops</a>
        </div>

        <div class="card">
            <h2>💰 Scholarships</h2>
            <p>Explore scholarship opportunities.</p>
            <a class="button" href="/scholarships">View Scholarships</a>
        </div>

        <a class="button" href="/logout">Logout</a>
    """
    return render_page("Student Dashboard", content)


# ---------------- STAFF DASHBOARD ----------------

@app.route("/staff")
def staff_dashboard():
    return render_page("Staff Dashboard", """
        <h1>👩‍🏫 Staff Dashboard</h1>
        <h2>Update Student Progress</h2>

        <form method="post" action="/update-progress">
            <label>Student Username</label>
            <input name="username" value="student1" required>

            <label>Marks (0-100)</label>
            <input type="number" name="marks"
                   min="0" max="100" required>

            <label>Attendance (0-100)</label>
            <input type="number" name="attendance"
                   min="0" max="100" required>

            <label>Points</label>
            <input type="number" name="points"
                   min="0" required>

            <button type="submit">Update Progress</button>
        </form>

        <a class="button" href="/logout">Logout</a>
    """)


@app.route("/update-progress", methods=["POST"])
def update_progress():
    username = request.form.get("username", "").strip()

    try:
        marks = int(request.form["marks"])
        attendance = int(request.form["attendance"])
        points = int(request.form["points"])
    except (ValueError, KeyError):
        return "Invalid input. Go back and try again.", 400

    if not username or not 0 <= marks <= 100:
        return "Invalid username or marks.", 400

    if not 0 <= attendance <= 100 or points < 0:
        return "Invalid attendance or points.", 400

    update_student(username, marks, attendance, points)

    return render_page("Updated", """
        <h1>✅ Student Progress Updated!</h1>
        <a class="button" href="/staff">Staff Dashboard</a>
        <a class="button" href="/student">Student Dashboard</a>
    """)


# ---------------- PARENT DASHBOARD ----------------

@app.route("/parent")
def parent_dashboard():
    student = get_student()

    content = f"""
        <h1>👨‍👩‍👧 Parent Dashboard</h1>

        <div class="card">
            <h2>Student Progress</h2>
            <p>Marks: {student['marks']}</p>
            <p>Attendance: {student['attendance']}%</p>
            <p>Points: {student['points']}</p>
        </div>

        <div class="card">
            <h2>📱 Mobile Usage</h2>
            <p>Sample daily usage: 2 hours</p>
            <p class="note">
                Demo value only. Actual phone usage is not tracked.
            </p>
        </div>

        <div class="card">
            <h2>⚠️ Alerts</h2>
            <p>Sample alert: Check your student's weekly progress.</p>
        </div>

        <a class="button" href="/logout">Logout</a>
    """
    return render_page("Parent Dashboard", content)


# ---------------- WORKSHOPS ----------------

@app.route("/workshops")
def workshop_page():
    content = "<h1>💻 Available Workshops</h1>"

    for index, workshop in enumerate(WORKSHOPS):
        content += f"""
            <div class="card">
                <h2>{workshop['name']}</h2>
                <p>Date: {workshop['date']}</p>
                <p>Mode: {workshop['mode']}</p>

                <form method="post" action="/register-workshop">
                    <input type="hidden" name="workshop_id"
                           value="{index}">
                    <input name="student_name"
                           placeholder="Enter your name" required>
                    <button type="submit">Register</button>
                </form>
            </div>
        """

    content += """
        <p class="note">Demo workshop details only.</p>
        <a class="button" href="/student">Back to Dashboard</a>
    """
    return render_page("Workshops", content)


@app.route("/register-workshop", methods=["POST"])
def register_workshop():
    try:
        index = int(request.form["workshop_id"])
        name = request.form["student_name"].strip()
        workshop = WORKSHOPS[index]
    except (ValueError, KeyError, IndexError):
        return "Invalid workshop details.", 400

    if not name:
        return "Enter your name.", 400

    registrations.append({
        "name": name,
        "workshop": workshop["name"]
    })

    return render_page("Registration", f"""
        <h1>✅ Registration Successful!</h1>
        <p>Student: {name}</p>
        <p>Workshop: {workshop['name']}</p>
        <p class="note">
            Demo registration only; no official booking was made.
        </p>
        <a class="button" href="/workshops">More Workshops</a>
        <a class="button" href="/student">Dashboard</a>
    """)


# ---------------- SCHOLARSHIPS ----------------

@app.route("/scholarships")
def scholarship_page():
    content = "<h1>💰 Scholarships</h1>"

    for index, scholarship in enumerate(SCHOLARSHIPS):
        content += f"""
            <div class="card">
                <h2>{scholarship['name']}</h2>
                <p>Eligibility: {scholarship['eligibility']}</p>
                <p>Deadline: {scholarship['deadline']}</p>

                <form method="post" action="/apply-scholarship">
                    <input type="hidden" name="scholarship_id"
                           value="{index}">
                    <input name="student_name"
                           placeholder="Enter your name" required>
                    <button type="submit">Apply</button>
                </form>
            </div>
        """

    content += """
        <p class="note">
            Demo listings only. Verify official eligibility and
            deadlines before applying. This is not an official
            scholarship application website.
        </p>
        <a class="button" href="/student">Back to Dashboard</a>
    """
    return render_page("Scholarships", content)


@app.route("/apply-scholarship", methods=["POST"])
def apply_scholarship():
    try:
        index = int(request.form["scholarship_id"])
        name = request.form["student_name"].strip()
        scholarship = SCHOLARSHIPS[index]
    except (ValueError, KeyError, IndexError):
        return "Invalid scholarship details.", 400

    if not name:
        return "Enter your name.", 400

    applications.append({
        "name": name,
        "scholarship": scholarship["name"]
    })

    return render_page("Application", f"""
        <h1>✅ Demo Application Submitted!</h1>
        <p>Student: {name}</p>
        <p>Scholarship: {scholarship['name']}</p>
        <p class="note">
            This does not submit an official scholarship application.
        </p>
        <a class="button" href="/scholarships">More Scholarships</a>
        <a class="button" href="/student">Dashboard</a>
    """)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)