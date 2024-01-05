import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database
db_path = "/home/coreyrichardson/mysite/courses.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
db = conn.cursor()

# CREATE TABLE users (id INTEGER, username TEXT NOT NULL UNIQUE, hash TEXT NOT NULL, PRIMARY KEY(id));
# CREATE TABLE courses (id INTEGER, user_id INTEGER NOT NULL, name TEXT NOT NULL UNIQUE, url TEXT, topics TEXT NOT NULL, desc TEXT NOT NULL, provider TEXT NOT NULL, is_complete BOOL NOT NULL, is_course BOOL NOT NULL, PRIMARY KEY(id));

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Display all courses the user has added to the database."""
    if request.method == "POST" and request.form.get("sort_index"):
        sort_index = request.form.get("sort_index")
        match sort_index:
            case "provider":
                courses = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = true ORDER BY provider, name",
                    (session["user_id"],)
                )
            case "completed":
                courses = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = true ORDER BY CASE is_complete WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 0 THEN 3 END",
                    (session["user_id"],)
                )
            case "inProgress":
                courses = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = true AND is_complete = 1",
                    (session["user_id"],)
                )
            case "incomplete":
                courses = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = true ORDER BY is_complete ASC",
                    (session["user_id"],)
                )
            case _: # name or anything else
                courses = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = true ORDER BY name",
                    (session["user_id"],)
                )

    else:
        courses = db.execute(
            "SELECT * FROM courses WHERE user_id = ? AND is_course = true ORDER BY name",
            (session["user_id"],)
        )

    courses = courses.fetchall()

    if len(courses) == 0:
        return render_template("empty.html", type="courses", action="display")

    return render_template("index.html", courses=courses, type="Courses")

@app.route("/modules", methods=["GET", "POST"])
@login_required
def modules():
    """Display modules the user has added to the database."""
    if request.method == "POST" and request.form.get("sort_index"):
        sort_index = request.form.get("sort_index")
        match sort_index:
            case "provider":
                modules = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = false ORDER BY provider, name",
                    (session["user_id"],)
                )
            case "is_complete DESC":
                modules = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = false ORDER BY is_complete DESC",
                    (session["user_id"],)
                )
            case "is_complete ASC":
                modules = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = false ORDER BY is_complete ASC",
                    (session["user_id"],)
                )
            case _: # name or anything else
                modules = db.execute(
                    "SELECT * FROM courses WHERE user_id = ? AND is_course = false ORDER BY name",
                    (session["user_id"],)
                )

    else:
        modules = db.execute(
            "SELECT * FROM courses WHERE user_id = ? AND is_course = false ORDER BY name",
            (session["user_id"],)
        )

    modules = modules.fetchall()

    if len(modules) == 0:
        return render_template("empty.html", type="modules", action="display")

    return render_template("index.html", courses=modules, type="Modules")

@app.route("/failure")
def failure():
    error_message = request.args.get("ERR_MSG", "Undefined Error.")
    return render_template("failure.html", ERR_MSG=error_message)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget an user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
             return redirect(url_for("failure", ERR_MSG="Username field was left empty."))
        if not request.form.get("password"):
            return redirect(url_for("failure", ERR_MSG="Password field was left empty."))

        users = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (request.form.get("username"),)
        ).fetchall()

        if len(users) != 1 or not check_password_hash(users[0][2], request.form.get("password")):
            return redirect(url_for("failure", ERR_MSG="Username or password invalid!"))

        session["user_id"] = users[0][0]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not username:
            return redirect(url_for("failure", ERR_MSG="Username field was left empty."))
        if not password:
            return redirect(url_for("failure", ERR_MSG="Password field was left empty."))
        if not confirm:
            return redirect(url_for("failure", ERR_MSG="Password confirmation field was left empty."))

        if password != confirm:
            return redirect(url_for("failure", ERR_MSG="Passwords didn't match."))

        password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (username, password,)
            )

            conn.commit()
        except ValueError:
            return redirect("failure", "Username already exists!")

        return redirect("/login")

    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    course_name = request.form.get("course_name")
    course_url = request.form.get("course_url") # OPTNL FIELD CAN BE MISSED FROM REQUEST!
    course_topics = request.form.get("topics")
    course_desc = request.form.get("desc")
    course_provider = request.form.get("provider")
    course_completed = request.form.get("completion")
    course_type = request.form.get("type")

    if request.method == "POST":
        if not course_name:
            return redirect(url_for("failure", ERR_MSG="Course name field was left empty."))
        if not course_topics:
            return redirect(url_for("failure", ERR_MSG="Topics covered field was left empty."))
        if not course_desc:
            return redirect(url_for("failure", ERR_MSG="Course description field was left empty."))
        if not course_provider:
            return redirect(url_for("failure", ERR_MSG="Course provider field was left empty."))
        if not course_completed:
            return redirect(url_for("failure", ERR_MSG="Course completion status field was left empty."))
        if not course_type:
            return redirect(url_for("failure", ERR_MSG="Course type field was left empty."))

        course_type = True if course_type == "true" else False

        if not course_url:
            db.execute(
                "INSERT INTO courses \
                (user_id, name, topics, desc, provider, is_complete, is_course) \
                VALUES (?, ?, ?, ?, ?, ?, ?)",
                (session["user_id"],
                course_name, course_topics, course_desc, course_provider, course_completed, course_type,)
            )
        else:
            db.execute(
                "INSERT INTO courses \
                (user_id, name, url, topics, desc, provider, is_complete, is_course) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (session["user_id"],
                course_name, course_url, course_topics, course_desc, course_provider, course_completed, course_type,)
            )

        conn.commit()

        if course_type: # course
            return redirect("/")
        else: # uni module
            return redirect("/modules")


    return render_template("add.html")

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():

    if request.method == "POST":
        # Course to update (reqd.)
        current_course_name = request.form.get("current_course_name")
        # Fields to update (optnl.)
        course_name = request.form.get("name")
        course_url = request.form.get("url")
        course_desc = request.form.get("desc")
        course_topics = request.form.get("topics")
        course_provider = request.form.get("provider")
        course_completed = request.form.get("completion")
        course_type = request.form.get("type")

        if not current_course_name:
            return redirect(url_for("failure", ERR_MSG="Course name field was left empty."))
        
        if course_url:
            db.execute(
                "UPDATE courses \
                SET url = ? \
                WHERE name = ? AND user_id = ?",
                (course_url, current_course_name, session["user_id"],)
            )
        
        if course_desc:
            db.execute(
                "UPDATE courses \
                SET desc = ? \
                WHERE name = ? AND user_id = ?",
                (course_desc, current_course_name, session["user_id"],)
            )
        
        if course_topics:
            db.execute(
                "UPDATE courses \
                SET topics = ? \
                WHERE name = ? AND user_id = ?",
                (course_topics, current_course_name, session["user_id"],)
            )
        
        if course_provider:
            db.execute(
                "UPDATE courses \
                SET provider = ? \
                WHERE name = ? AND user_id = ?",
                (course_provider, current_course_name, session["user_id"],)
            )
        
        if course_completed:
            db.execute(
                "UPDATE courses \
                SET is_complete = ? \
                WHERE name = ? AND user_id = ?",
                (course_completed, current_course_name, session["user_id"],)
            )

        if course_type:
            course_type = True if course_type == "true" else False
            db.execute(
                "UPDATE courses \
                SET is_course = ? \
                WHERE name = ? AND user_id = ?",
                (course_type, current_course_name, session["user_id"],)
            )
        
        # Name must be changed last
        if course_name:
            db.execute(
                "UPDATE courses \
                SET name = ? \
                WHERE name = ? AND user_id = ?",
                (course_name, current_course_name, session["user_id"],)
            )
        
        conn.commit()    
        return redirect("/")

    names = db.execute(
        "SELECT name FROM courses WHERE user_id = ? ORDER BY is_course, name",
        (session["user_id"],)
    ).fetchall()
    
    if len(names) == 0:
        return render_template("empty.html", type="entries", action="update")

    return render_template("update.html", names=names)


@app.route("/drop", methods=["GET", "POST"])
@login_required
def drop():

    if request.method == "POST":
        course_name = request.form.get("course_name")

        if not course_name:
            return redirect(url_for("failure", ERR_MSG="Course name field was left empty."))

        db.execute(
            "DELETE FROM courses \
            WHERE name = ? AND user_id = ?",
            (course_name, session["user_id"],)
        )

        conn.commit()

        return redirect("/")


    names = db.execute(
        "SELECT name FROM courses WHERE user_id = ? ORDER BY is_course, name",
        (session["user_id"],)
    ).fetchall()
    
    if len(names) == 0:
        return render_template("empty.html", type="entries", action="drop")

    return render_template("drop.html", names=names)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not current_password:
            return redirect(url_for("failure", ERR_MSG="Username field was left empty."))
        if not new_password:
            return redirect(url_for("failure", ERR_MSG="Username field was left empty."))
        if not confirm_password:
            return redirect(url_for("failure", ERR_MSG="Username field was left empty."))

        user = db.execute(
            "SELECT * FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchall()

        if not check_password_hash(user[0][2], current_password):
            return redirect(url_for("failure", ERR_MSG="Password was incorrect."))
        if new_password != confirm_password:
            return redirect(url_for("failure", ERR_MSG="Passwords did not match."))

        db.execute(
            "UPDATE users \
            SET hash = ? \
            WHERE id = ?",
            (generate_password_hash(new_password), session["user_id"],)
        )

        conn.commit()

        return render_template("success.html")

    return render_template("change_password.html")

@app.route("/skills")
@login_required
def skills():
    course_topics = db.execute(
        "SELECT topics FROM courses \
        WHERE user_id = ? AND is_complete = true",
        (session["user_id"],)
    ).fetchall()
    
    if len(course_topics) == 0:
        return render_template("empty.html", type="skills", action="display")
    
    topics = {}
    
    # course_topics = [('Python, OOP',), ('CompSci, C, Python, HTML, CSS, JS, SQL',)]
    for skill_tuple in course_topics:
        skill_tuple_contents = skill_tuple[0]
        skill_list = skill_tuple_contents.split(",")
        for skill in skill_list:
            skill = skill.strip()
            if skill in topics:
                topics[skill] += 1
            else:
                topics[skill] = 1
                    
    skills = sorted(topics.items(), key=lambda x: (-x[1], x[0]))

    return render_template("skills.html", skills=skills)
    