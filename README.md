# course-progress-tracker
A Flask web application that can be used to track which courses and university modules I have completed and which I have yet to finish. It also features a 'learning log' where I can use a FlaskForm to create blog posts in order to record my progress.

---

## Contents

- [Software Installation Guide](#software-installation-guide)
- [Software Description](#software-description)
    - [pages](#pages)
        - [index-page](#index-page)
        - [view-university-modules](#view-university-modules)
        - [learning-log](#learning-log)
        - [add-or-modify-a-course](#add-or-modify-a-course)
    - [html-and-css](#html-and-css)
        - [base-template](#base-template)
        - [style.css](#stylecss)
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
pip install Flask Flask-WTF
```

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

### Index Page

The index page is the default homepage of this Flask web application. It reads and displays each course and information related to the course from `static/courses.json`.

![](/res/index.jpg)

The index page takes an optional URL parameter `status`.
```py
@app.route('/', methods=["GET","POST"], defaults={'status' : "all"})    
@app.route('/<status>', methods=["GET","POST"])
def index(status):
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

![](/res/flow_diagrams/Index.svg)

Parameter | Summary | Result
--- | --- | ---
`"alphabetical"` | Displays all courses ordered alphabetically by course name. | ![](/res/alphabetical.jpg)
`"by_provider"` | Displays all courses ordered alphabetically by course provider name. | ![](/res/by_provider.jpg)
`"complete"` | Displays the subset of the courses which have been marked as completed. | ![](/res/complete.jpg)
`"uncomplete"` | Displays the subset of the courses which have been marked as not completed.  | ![](/res/uncomplete.jpg)

- [`app.py::index`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/app.py#L38C3-L38C3)
- [`templates/index.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/index.html)
- [`static/courses.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/courses.json)

### View University Modules

The View University Modules page can be found at `127.0.0.1:5000/uni_modules` (or equivalent). It reads and displays each course and information related to the course from `static/modules.json`.

![](/res/uni_modules.jpg)

The View University Modules page takes an optional URL parameter `year`.
```py
@app.route('/uni_modules', methods=["GET","POST"], defaults={"year" : "all"})
@app.route('/uni_modules/<year>', methods=["GET","POST"])
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

- [`app.py::uni_modules`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/app.py#L76)
- [`templates/uni_modules.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/uni_modules.html)
- [`static/modules.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/modules.json)

### Learning Log

The View University Modules page can be found at `127.0.0.1:5000/learning_log` (or equivalent). It featues a 'Create a New Post' form and reads and displays the posts from `static/posts.json`, reverse ordered by datetime of posting (newest to oldest).

![](/res/learning_log.jpg)

![](/res/flow_diagrams/Learning_Log.svg)

- [`app.py::view_log`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/app.py#L198)
- [`forms.py::AddToLog`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/forms.py#L56)
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

- [`app.py::add`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/app.py#L111)
- [`forms.py::AddCourse`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/forms.py#L9)
- [`forms.py::CourseCompleted`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/forms.py#L22)
- [`forms.py::ModuleCompleted`](https://github.com/corey-richardson/course-progress-tracker/blob/ce296945d6023d4de590ccac313a6e83b65a193c/forms.py#L42C4-L42C4)
- [`templates/add.html`](https://github.com/corey-richardson/course-progress-tracker/blob/main/templates/add.html)
- [`static/courses.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/courses.json)
- [`static/uni_modules.json`](https://github.com/corey-richardson/course-progress-tracker/blob/main/static/uni_modules.json)

---

## HTML and CSS

The HTML structure files can be found in the [`templates`](/templates/) directory. The CSS styling file can be found at [`static/style.css`](/static/style.css).

[`templates/`](/templates/)
- [`add.html`](/templates/add.html)
- [`base.html`](/templates/base.html)
- [`index.html`](/templates/index.html)
- [`learning_log.html`](/templates/learning_log.html)
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

```py
# Example of a test in 'test_forms.py'
def test_AddCourse_empty():
    with app.test_request_context("/add"):
        form = AddCourse()
        assert not form.validate()
        assert form.errors
```

To run the unit testing:

1. Check that *"Learn Python 3"* is present as a course name in [`courses.json`](/static/courses.json).
2. Check that *"Learn Skydiving for Beginners"* is **NOT** present as a course name in [`courses.json`](/static/courses.json).
3. Check that *""Software Engineering 1"* is present as a module name in [`modules.json`](/static/modules.json).
4. Check that *"Learn Skydiving for Beginners"* is **NOT** present as a module name in [`modules.json`](/static/modules.json).
5. Either run the bash script [`run_tests.sh`](/tests/run_tests.sh) OR in the terminal type:
```
source bin/activate
pytest -v --no-header tests/test_forms.py | tee tests/results.txt
deactivate
```
6. Navigate to [`tests/results.txt`](/tests/results.txt) and ensure all tests pass.

- [`tests/test_forms.py`](/tests/test_forms.py)
- [`tests/run_tests.sh`](/tests/run_tests.sh)
- [`tests/results.txt`](/tests/results.txt)

---

## File Structure

The layout of the project should look as follows *(venv/documentation files omitted)*:
```
static/
    courses.json
    modules.json
    posts.json
    style.css
templates/
    add.html
    base.html
    index.html
    learning_log.html
    uni_modules.html
tests/
    results.txt
    run_tests.sh
    test_forms.py
app.py
forms.py
```
