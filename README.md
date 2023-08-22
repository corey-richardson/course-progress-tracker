# course-progress-tracker
A Flask web application that can be used to track which courses and university modules I have completed and which I have yet to finish. It also features a 'learning log' where I can use a FlaskForm to create blog posts in order to record my progress. It includes user authentication for individual account tracking.

---

## Contents

- [Software Installation Guide](#software-installation-guide)
- [Software Description](#software-description)
    - [pages](#pages)
        - [login-page](#login-page)
        - [registration-page](#registration-page)
        - [homepage](#homepage)
        - [view-university-modules](#view-university-modules)
        - [learning-log](#learning-log)
        - [add-or-modify-a-course](#add-or-modify-a-course)
    - [html-and-css](#html-and-css)
        - [base-template](#base-template)
        - [stylecss](#stylecss)
    - [pytest-unit-testing](#pytest-unit-testing)
    - [file-structure](#file-structure)

---

# Software Installation Guide

This guide will walk you through the steps to set up and run the "Course Progress Tracker" project on your local machine.

## Prerequisites
Before you begin, ensure that you have the following installed on your system:
- Python (version 3.6 or later) *(3.10.8 recommended)*
- Git

## Step 1: Clone the Repository

1. Open your terminal or command prompt.

2. Navigate to the directory where you want to store the project.

3. Run the following command to clone the repository:
```bash
git clone https://github.com/corey-richardson/course-progress-tracker.git
```

## Step 2: Install Required Packages

1. Navigate to the project directory:
```bash
cd course-progress-tracker
```

2. Create a virtual environment (recommended but optional):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows
```bash
venv\Scripts\activate
```
- Linux, maxOS, GitHub Codespace
```bash
source venv/bin/activate
```

4. Install required packages using pip:
```bash
pip install Flask Flask-WTF pytest pytest-flask
```

5. Run the `pytest` command below.
```bash
pytest -v --no-header | tee tests/results.txt
```
> The `pytest` tests will run, and you will see the test output in the terminal as well as in the `results.txt` file in the `test/` directory.

## Step 3: Run the Flask Application

1. In the project directory, you'll find a file named app.py. This is the main Flask application file.

2. Run the application using the following command:
```bash
flask run
```
> By default, the application should start on [127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.

3. Open your web browser and navigate to [127.0.0.1:5000/](http://127.0.0.1:5000/). You should see the "Course Progress Tracker" application running.
---

## Step 4: Stopping the Application

1. To stop the Flask application, go back to the terminal where the application is running and press <kbd>Ctrl</kbd>+<kbd>C</kbd>.

2. If you used a virtual environment, you can deactivate it by running:
```bash
deactivate
```

You've successfully installed and run the "Course Progress Tracker" project on your local machine.

# Software Description

## Pages

### Login Page

The Login page is the default index page and can be found at `127.0.0.1:5000/` (or equivalent). This page features the 'LoginForm', the output of which is compared against the account stored in `static/accounts.json`. If successful, the user is logged in.

![](/res/login.JPG)

### Registration Page

The Register page can be found at `127.0.0.1:5000/register`(or equivalent). It features the `RegistrationForm`, the output of which is written to `static/accounts.json` if the form successfully validates.

The requirements for validation include:
- Username required
- Password required
- Repeat Password required
- Username must not contain spaces
- Username must be unique
- Password and Repeat Password must match
- Password must not contain spaces
- Password must be a minimum of 8 characters
- Password must contain a lowercase character
- Password must contain an uppercase character
- Password must contain a punctuation character

![](/res/register.JPG)

### Homepage

Once the user successfully logs in or registers, they are redirected to the homepage. This is found at `127.0.0.1:5000/homepage`(or equivalent).

This page displays each course and related information that the user has added via the '/add' route. 

The homepage is login-protected and takes an optional URL parameter `status`.
```py
@app.route('/', methods=["GET","POST"], defaults={'status' : "all"})    
@app.route('/<status>', methods=["GET","POST"])
@login_required
def homepage(status):
    ...
```

This parameter is used to decide how to display the courses; the default is to display all courses in the order they are defined.
```py
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
```

![](/res/homepage.JPG)

Parameter | Summary | Result
--- | --- | ---
`"alphabetical"` | Displays all courses ordered alphabetically by course name. | ![](/res/alphabetical.jpg)
`"by_provider"` | Displays all courses ordered alphabetically by course provider name. | ![](/res/by_provider.jpg)
`"complete"` | Displays the subset of the courses which have been marked as completed. | ![](/res/complete.jpg)
`"uncomplete"` | Displays the subset of the courses which have been marked as not completed.  | ![](/res/uncomplete.jpg)

- [`templates/index.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/index.html)
- [`static/courses.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/courses.json)

### View University Modules

The View University Modules page can be found at `127.0.0.1:5000/uni_modules` (or equivalent). It reads and displays each course and information related to the course from `static/modules.json` linked to the current user.

The View University Modules page is login-protected and takes an optional URL parameter `year`.
```py
@app.route('/uni_modules', methods=["GET","POST"], defaults={"year" : "all"})
@app.route('/uni_modules/<year>', methods=["GET","POST"])
@login_required
def uni_modules(year):
    ...
```

This parameter is used to decide how to display the courses; the default is to display all courses in the order they are defined.
```py
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
```

![](/res/flow_diagrams/Uni_Modules.svg)

Parameter | Summary | Result
--- | --- | ---
`"first"` | Displays the subset of the modules from the first year of study. | ![](/res/uni_modules_first.jpg)
`"second"` | Displays the subset of the modules from the second year of study. | ![](/res/uni_modules_second.jpg)
`"placement`" | Displays the subset of the modules from the optional placement year of the course. | ![](/res/uni_modules_placement.jpg)
`"final"` | Displays the subset of the modules from the final year of study. | ![](/res/uni_modules_final.jpg)

- [`templates/uni_modules.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/uni_modules.html)
- [`static/modules.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/modules.json)

### Learning Log

The Learning Log page can be found at `127.0.0.1:5000/learning_log` (or equivalent).

The Learning Log Modules page is login-protected and takes an optional URL parameter `visibility`.

```py
@app.route('/learning_log', methods=["GET","POST"], defaults={'visibility':'my'})
@app.route('/learning_log/<visibility>', methods=["GET","POST"])
@login_required
def view_log(visibility):
    ...
```

This variable controls which posts get displayed.
- `my` - only view posts linked to the `current_user`. This page also contains the `AddToLog` form where the user can create new posts.
- `search` - Features the `SearchUser` form allowing the user to view posts from a specific user.
- `all` or `_` (default) - view all posts, irrespective of poster.
```py
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
```

![](/res/learning_log.jpg)

![](/res/flow_diagrams/Learning_Log.svg)

- [`templates/learning_log.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/learning_log.html)
- [`static/posts.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/posts.json)

### Add or Modify a Course

The Add or Modify a Course page can be found at `127.0.0.1:5000/add` (or equivalent). It features three forms:

Add a New Course - `AddCourse`
- Allows the user to add a new online course to the database in `courses.json`.

Modify Online Courses - `CourseCompleted`
- Allows the user to change the status of a pre-existing course between completed and not completed. 

Modify University Modules - `ModuleCompleted`
- Allows the user to change the status of a university module between completed and not completed.

![](/res/add.jpg)

![](/res/flow_diagrams/Add.svg)

---

## HTML and CSS

The HTML structure files can be found in the [`templates`](/templates/) directory. The CSS styling file can be found at [`static/style.css`](/static/style.css).

[`templates/`](/templates/)
- [`add.html`](/templates/add.html)
- [`base.html`](/templates/base.html)
- [`homepage.html`](/templates/homepage.html)
- [`index.html`](/templates/index.html)
- [`learning_log.html`](/templates/learning_log.html)
- [`register.html`](/templates/register.html)
- [`uni_modules.html`](/templates/uni_modules.html)

[`static/`](/static/)
- [`style.css`](/static/style.css)

### Base Template

The base template is used across each page of the web application. It features the header, navigation bar and footer. It also links the CSS styling file to the templates.

- [`templates/base.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/base.html)

### style.css

All elements follow the "Lucida Sans Unicode" `font-family`. <br>
Colour variables `text`, `subtext`, `background`, `primary`, `second` and `accent` are defined in root. `green` and `red` are also defined for use by the `.dot` class.
```css
:root {
    --text: #03272a;
    --subtext: #5c8f94;
    --background: #def9fc;
    --primary: #c2f4fa;
    --secondary: #95f3fd;
    --accent: #12c9de;
    --green: #0F0;
    --red: #F00;
  }
  
* {
    font-family: "Lucida Grande", "Lucida Sans Unicode";
    color: var(--text);
    padding: 0;
}
```

Courses and modules are encapsulated using the `course-container` and `container-text` classes. 
```css
.course-container {
    background-color: var(--primary);
    border: solid var(--accent);
    border-radius: 5px;
    margin: 5px 0;
}
  
.container-text {
    margin: 0 20px;
}
```

Navigational links `<a>` are encapsulated with the `nav-container` class.
```css
.nav-container a {
    width: 20%;
    background-color: var(--primary);
    border: solid var(--accent);
    border-radius: 5px;
    padding: 0 5px;
    font-weight: bold;
    text-align: center;
    flex-grow: 1;
    margin: 5px 0;
    margin-right: 10px;
}
  
.nav-container a:last-child {
    margin-right: 0;
}
  
.nav-container span {
    display: flex;
}
```

- [`static/style.css`](/static/style.css)

---

## Pytest Unit Testing

Pytest is used to test the FlaskForm objects employed in the web application. Condtions tested are:
- empty form input
- valid form input
- invalid form input
- missing required field
- username is valid
- password is valid
- protected routes can't be accessed

```py
# Example of a test in 'test_forms.py'
def test_AddCourse_empty():
    '''
    Test an empty AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
        form = AddCourse()
        assert not form.validate()
        assert form.errors
```

To run the unit testing:

1. Check that *"Test Course"* is present as a course name in [`courses.json`](/static/courses.json), linked to `'TEST_ACCOUNT_DONT_DELETE`.
2. Check that *"Learn Skydiving for Beginners"* is **NOT** present as a course name in [`courses.json`](/static/courses.json), linked to `'TEST_ACCOUNT_DONT_DELETE`.
3. Check that *"Test Module"* is present as a module name in [`modules.json`](/static/modules.json), linked to `'TEST_ACCOUNT_DONT_DELETE`.
4. Check that *"Learn Skydiving for Beginners"* is **NOT** present as a module name in [`modules.json`](/static/modules.json), linked to `'TEST_ACCOUNT_DONT_DELETE`.
5. Either run the bash script [`run_tests.sh`](/tests/run_tests.sh) OR in the terminal type:
```
source bin/activate
pytest -v --no-header | tee tests/results.txt
deactivate
```
6. Navigate to [`tests/results.txt`](/tests/results.txt) and ensure all tests pass.

- [`tests/test_forms.py`](/tests/test_forms.py)
- [`tests/test_authentication.py`](/tests/test_authentication.py)
- [`tests/run_tests.sh`](/tests/run_tests.sh)
- [`tests/results.txt`](/tests/results.txt)

> In this version of the software, there are 33 tests.

---

## File Structure

The layout of the project should look as follows *(venv/documentation files omitted)*:
```
static/
    accounts.json
    courses.json
    modules.json
    posts.json
    style.css
templates/
    add.html
    base.html
    homepage.html
    index.html
    learning_log.html
    register.html
    uni_modules.html
tests/
    results.txt
    run_tests.sh
    test_forms.py
    test_authentication.py
app.py
authenticate.py
forms.py
```
