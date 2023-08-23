from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, redirect, url_for, flash

from forms import (
    CourseCompleted, 
    ModuleCompleted, 
    AddCourse, 
    AddToLog, 
    DateRange,
    SearchUser)
from authenticate import (
    LoginForm, 
    RegistrationForm)

from datetime import datetime
import json

COURSE_FILE_PATH = "static/courses.json"
MODULE_FILE_PATH = "static/modules.json"
POSTS_FILE_PATH = "static/posts.json"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def load_user(user_id):
    # Replace this with actual loading logic from your JSON file
    with open('static/accounts.json', 'r') as file:
        users = json.load(file)["account list"]
        for user in users:
            if user['username'] == user_id:
                return User(user_id)
            
@app.context_processor
def inject_year():
    from datetime import date
    year = date.today().strftime("%Y")
    return dict(year = year)

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

def get_all(courses, condition, status):
    '''
    Return all the courses where 'condition' is 'status'
    
    courses: Either 'courses' or 'modules'
    condition: property of each course/module to check against
    status: desired value of condition
    
    e.g. get_all(courses, "completed", "true") returns all courses which have
    been marked as completed.
    '''
    temp = []
    for course in courses:
        if course[condition] == status:
            temp.append(course)
    return temp

@app.route('/', methods=["GET","POST"])
def index():
    
    with open("static/accounts.json", "r") as acc:
        accounts = json.load(acc)["account list"]
    
    login = LoginForm()
    
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data
        
        account_found = False
        
        for account in accounts:
            if account["username"] == username:
                account_found = True
                
                if check_password_hash(account["password"], password):
                    user = User(username)
                    login_user(user)
                    return redirect(url_for("homepage"))
                else:
                    flash("Incorrect password. Please try again.", "danger")

        if not account_found:
            flash("Account not found. Please try again.", "danger")
    
    return render_template(
        "index.html",
        login = login,
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    with open("static/accounts.json", "r") as acc:
        accounts = json.load(acc)
    
    register = RegistrationForm(csrf_enabled=False)

    if register.validate_on_submit():
        username = register.username.data
        password = generate_password_hash(register.password.data)
        
        new_user = {
            "username": f"{username}",
            "password": f"{password}"
        }
        
        accounts["account list"].append(new_user)
        with open("static/accounts.json", "w") as acc:
            json.dump(accounts, acc, indent = 4)
            
        register.update()
        
        user = User(username)
        login_user(user)
                        
        return redirect(url_for("homepage"))

    return render_template(
        'register.html', 
        register=register)
        
@app.route('/homepage', methods=["GET","POST"], defaults={'status' : "all"})    
@app.route('/<status>', methods=["GET","POST"])
@login_required
def homepage(status):
    '''
    Homepage / Index page
    
    Displays all courses read in from 'courses.json'
    Functionality can be altered using URL variables to only display subsets
    of courses OR courses ordered alphabetically.
    '''
    # Open 'courses.json' and read into a dict.
    with open(COURSE_FILE_PATH, "r") as j:
            courses = json.load(j)["course list"]
            
    courses = get_all(courses, "owner", current_user.id)
    
    # Compare URL variable 'status'
    match status:
        case "alphabetical":
            # Sort all courses alphabetically
            courses.sort(key = lambda c: c["name"])
        case "by_provider":
            # Sort all courses by provider
            courses.sort(key = lambda c: c["provider"])
        case "complete":
            # Query only the courses marked as completed
            courses = get_all(courses, "completed", "true")
        case "uncomplete":
            # Query only the courses marked as incompleted
            courses = get_all(courses, "completed", "false")
        case _:
            pass
          
    return render_template(
        "homepage.html",
        course_list = courses,
        current_user = current_user,
    )
    
@app.route('/uni_modules', methods=["GET","POST"], defaults={"year" : "all"})
@app.route('/uni_modules/<year>', methods=["GET","POST"])
@login_required
def uni_modules(year):
    '''
    View University Modules page
    
    Displays all modules read in from 'modules.json'
    Functionality can be altered using URL variables to only display subsets
    of modules by year of study.
    '''
    # Open 'modules.json' and read into a dict.
    with open(MODULE_FILE_PATH, "r") as j:
        modules = json.load(j)["module list"]
    
    modules = get_all(modules, "owner", current_user.id)
    
    # Compare URL variable 'year'
    match year:
        # Query only modules from first year
        case "first":
            modules = get_all(modules, "year", "First")
        # Query only modules from first year
        case "second":
            modules = get_all(modules, "year", "Second")
        # Query only the placement year
        case "placement":
            modules = get_all(modules, "year", "Placement")
        # Query only modules from the final year
        case "final":
            modules = get_all(modules, "year", "Final")
        case _:
            pass
         
    return render_template(
        "uni_modules.html",
        modules_list = modules,
        current_user = current_user
    )
    
@app.route('/add', methods=["GET","POST"])
@login_required
def add():
    
    # Read courses and modules from 'courses.json' and 'modules.json' into
    # their respective dictionaries
    with open(COURSE_FILE_PATH, "r") as j:
            courses = json.load(j)       
    with open(MODULE_FILE_PATH, "r") as j:
            modules = json.load(j)
    
    # Initialise the forms used on this page
    # 'completed_course_form' has the method 'update_course_choices()' 
    # which allows the course selection to update as new courses are 
    # added by 'add_course'
    add_course = AddCourse()
    completed_course_form = CourseCompleted()
    completed_course_form.update_course_choices()
    completed_module_form = ModuleCompleted()
    
    # When 'add_course' is successfully submitted...
    if add_course.validate_on_submit():
        # Set vars from field data
        name = add_course.name.data
        desc = add_course.desc.data
        url = add_course.url.data
        provider = add_course.provider.data
        length = add_course.length.data
        section = add_course.section.data
        completed = add_course.completed.data
        owner = add_course.owner.data
        # Format data to be appended to json
        data = {
            "name" : f"{name}",
            "desc" : f"{desc}",
            "url"  : f"{url}",
            "provider" : f"{provider}",
            "length" : f"{length}",
            "section" : f"{section}",
            "completed" : f"{completed}",
            "owner" : f"{owner}"}
        # Append the new course data to the existing course dict        
        courses["course list"].append(data)
        # Write the update dict to the json file (non-volatile storage)
        with open(COURSE_FILE_PATH, "w") as j:
            json.dump(courses, j, indent=4)
        # Redirect to the homepage to view the new course in the list    
        return redirect(url_for("index"))

    # When 'completed_course_form' is successfully submitted...
    if completed_course_form.validate_on_submit():
        # Set vars from field data
        status = completed_course_form.status.data
        course_to_modify = completed_course_form.completed_course.data
        # For each course check if the 'name' attribute matches the target name
        # If yes, update the 'completed' attribute to the new value, then break.
        for course in courses["course list"]:
            if course["name"] == course_to_modify:
                course["completed"] = status
                break
        # Write the updated data to the relevant json file.    
        with open(COURSE_FILE_PATH, "w") as j:
            json.dump(courses, j, indent=4)     
    
    # When 'completed_module_form' is successfully submitted...
    if completed_module_form.validate_on_submit():
        # Set vars from field data
        status = completed_module_form.status.data
        module_to_modify = completed_module_form.completed_module.data   
        # For each module check if the 'name' attribute matches the target name
        # If yes, update the 'completed' attribute to the new value, then break.
        for module in modules["module list"]:
            if module["name"] == module_to_modify:
                module["completed"] = status
                break
        # Write the updated data to the relevant json file.     
        with open(MODULE_FILE_PATH, "w") as j:
            json.dump(modules, j, indent=4)    
            
        # D.R.Y oppurtunity ^
        
    return render_template(
        "add.html",
        course_list = courses["course list"],
        add_course = add_course,
        completed_course_form = completed_course_form,
        modules_list = modules["module list"],
        completed_module_form = completed_module_form,
        current_user = current_user
    )

@app.route('/learning_log', methods=["GET","POST"], defaults={'visibility':'my'})
@app.route('/learning_log/<visibility>', methods=["GET","POST"])
@login_required
def view_log(visibility):
    
    # Initialise forms
    add_to_log = AddToLog()
    date_range = DateRange()
    search_user = SearchUser()
    
    with open(POSTS_FILE_PATH, "r") as j:
            posts = json.load(j)

    match visibility:
        case "my":       
            posts = get_all(posts, "owner", current_user.id)
        case "search":
            if search_user.validate_on_submit():
                user_to_search = search_user.user_to_search.data
                posts = get_all(posts, "owner", user_to_search)
        case _:
            with open('static/accounts.json', 'r') as file:
                users = json.load(file)["account list"]
                for user in users:
                    if user['username'] == visibility:
                        posts = get_all(posts, "owner", visibility)
            # else view everyones posts
    
    # Sort posts by datetime        
    posts.sort(key = lambda p: p["sort_time"], reverse=True)
    
    if date_range.validate_on_submit():
        start_date = datetime.combine(date_range.start_date.data, datetime.min.time())
        end_date = datetime.combine(date_range.end_date.data, datetime.max.time())
        temp = []
        for post in posts:
            p = datetime.strptime(post["sort_time"], "%Y-%m-%d %H:%M:%S.%f")
            if p >= start_date and p <= end_date:
                temp.append(post)
        posts = temp.copy()
    
    # When 'add_to_log' is successfully submitted...
    if add_to_log.validate_on_submit():
        # Set vars from field data
        title = add_to_log.title.data
        project = add_to_log.project.data
        topics = add_to_log.topics.data
        body = add_to_log.body.data
        # Optional inputs
        try:
            link_title = add_to_log.link_title.data
            link = add_to_log.link.data
        except AttributeError:
            link_title = None
            link = None
        # Get current date times and format
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M")
        sort_time = datetime.now()
        owner = current_user.id
        
         # Format data to be appended to json
        data = {
            "title" : f"{title}",
            "project" : f"{project}",
            "topics" : f"{topics}",
            "body"  : f"{body}",
            "link_title" : f"{link_title}",
            "link" : f"{link}",
            "date" : f"{date}",
            "time" : f"{time}",
            "sort_time" : f"{sort_time}",
            "owner" : f"{owner}"}
        # Append the new post data to the existing post dict        
        posts.append(data)
        # Write the update dict to the json file (non-volatile storage)
        with open(POSTS_FILE_PATH, "w") as j:
            json.dump(posts, j, indent=4)
        
        # Refresh  
        return redirect(url_for("view_log"))
            
    return render_template(
        "learning_log.html",
        posts = posts,
        add_to_log = add_to_log,
        date_range = date_range,
        current_user = current_user,
        visibility = visibility,
        search_user = search_user,
        
    )
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized():
  # do stuff
  return "Sorry you must be logged in to view this page<br> Return to <a href='/'>Home</a>"
