from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField, 
    TextAreaField, 
    URLField, 
    SelectField, 
    DateField, 
    SubmitField)

from wtforms.validators import DataRequired, ValidationError
import json
from datetime import datetime

import os
here = os.path.dirname(__file__)

COURSE_FILE_PATH = "data/courses.json"
MODULE_FILE_PATH = "data/modules.json"
POSTS_FILE_PATH = "data/posts.json"
ACCOUNTS_FILE_PATH = "data/accounts.json"

COURSE_FILE_PATH = os.path.join(here, COURSE_FILE_PATH)
MODULE_FILE_PATH = os.path.join(here, MODULE_FILE_PATH)
POSTS_FILE_PATH = os.path.join(here, POSTS_FILE_PATH)
ACCOUNTS_FILE_PATH = os.path.join(here, ACCOUNTS_FILE_PATH)

# , render_kw={"placeholder": "Set post title..."}

class AddCourse(FlaskForm):
    name = StringField(
        "Course Name: ", 
        validators=[DataRequired()])
    desc = TextAreaField(
        "Course Description: ", 
        validators=[DataRequired()])
    url = URLField(
        "Course Link: ", 
        validators=[DataRequired()])
    provider = StringField(
        "Course Provider: ", 
        validators=[DataRequired()])
    length = StringField(
        "Course Duration: ", 
        validators=[DataRequired()])
    section = StringField(
        "Topic: ", 
        validators=[DataRequired()])  
    completed = SelectField(
        "Have you completed this course? ", 
        choices=[
            ("true","Yes"),
            ("false","No")], 
        default="false")
    
    submit = SubmitField()

class AddModule(FlaskForm):
    
    name = StringField(
        "Module Name: ", 
        validators=[DataRequired()])
    
    desc = TextAreaField(
        "Module Description: ", 
        validators=[DataRequired()])
    
    code = StringField(
        "Module Code: ", 
        validators=[DataRequired()])
    
    year = SelectField(
        "Year of Study: ",
        choices=[
            "First",
            "Second",
            "Third",
            "Placement",
            "Final",
        ],
        validators=[DataRequired()])
    
    optional = SelectField(
        "Is the module optional? ", 
        choices=[
            ("true","Yes"),
            ("false","No")], 
        default="false",
        validators=[DataRequired()])  
    
    completed = SelectField(
        "Have you completed this mdoule? ", 
        choices=[
            ("true","Yes"),
            ("false","No")], 
        default="false",
        validators=[DataRequired()])
    
    submit = SubmitField()
    
class CourseCompleted(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(CourseCompleted, self).__init__(*args, **kwargs)
        self.update_course_choices() 
    # Method to update the 'choices_list' list. Called on instance 
    # initialisation and on page load to ensure list contains any courses 
    # that were just added by the AddCourse form.
    def update_course_choices(self):
        with open(COURSE_FILE_PATH, "r") as j:
            courses = json.load(j)["course list"]   
        choices_list = [course["name"] for course in courses if course["owner"] == current_user.id]
        if not choices_list:
            choices_list.append(('placeholder', 'No courses found'))
        self.completed.choices = sorted(choices_list)
        
    status = SelectField(
        "Status: ",
        choices=[
            ("true","finished"),
            ("false","unfinished")],
        validators=[DataRequired()])
    completed = SelectField(
        "Mark Course as Completed:", 
        validators=[DataRequired()])
    
    submit = SubmitField()
    
class ModuleCompleted(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(ModuleCompleted, self).__init__(*args, **kwargs)
        self.update_module_choices() 
        
    def update_module_choices(self):    
        with open(MODULE_FILE_PATH, "r") as j:
            modules = json.load(j)["module list"]    
        choices_list = [module["name"] for module in modules if module["owner"] == current_user.id]
        if not choices_list:
            choices_list.append(('placeholder', 'No modules found'))
        self.completed.choices = sorted(choices_list)
        
    status = SelectField(
        "Status: ",
        choices=[
            ("true","finished"),
            ("false","unfinished")],
        validators=[DataRequired()])
    completed = SelectField(
        "Mark Course as Completed:", 
        validators=[DataRequired()],
        )
    
    submit = SubmitField()

class LinkAndLinkTitleRequiredTogether:
    def __init__(self, message=None):
        self.message = message
        
    def __call__(self, form, field):
        link_title_data = form.link_title.data
        link_data = form.link.data

        if (link_title_data and not link_data) or (link_data and not link_title_data):
            if self.message is None:
                message = "Both Link and Link Title must be set together or neither should be set"
            else:
                message = self.message
            raise ValidationError(message)
        
class AddToLog(FlaskForm):
    
    title = StringField(
        "*Title: ", 
        validators=[DataRequired()])
    project = StringField(
        "*Project or Course Name: ", 
        validators=[DataRequired()])
    topics = StringField(
        "*Topics Covered: ", 
        validators=[DataRequired()])
    body = TextAreaField(
        "*Post Contents: ", 
        validators=[DataRequired()])
    
    link_title = StringField("Link Title: ")
    link = URLField("Link URL: ")
    submit = SubmitField()

    link_and_link_title_validator = LinkAndLinkTitleRequiredTogether()

    # Override the validate on submit method to perform additional custom
    # validation on 'link_title' and 'link'
    def validate_on_submit(self):
        if not super().validate():
            return False
        
        try:
            self.link_and_link_title_validator(self, self.link)
        except ValidationError:
            self.link_title.errors.append("Both Link and Link Title must be set together or neither should be set")
            self.link.errors.append("Both Link and Link Title must be set together or neither should be set")
            return False

        return True
    
class DateRange(FlaskForm):
    # Only runs once when flask app is first enabled
    with open(POSTS_FILE_PATH, "r") as j:
        posts = json.load(j)
    
    earliest_datetime = min(
        posts, 
        key=lambda x: datetime.strptime(
            x["sort_time"], "%Y-%m-%d %H:%M:%S.%f"))

    start_date = DateField(
        "Start Date: ", 
        validators=[DataRequired()], 
        default = datetime.strptime(
            earliest_datetime["sort_time"], "%Y-%m-%d %H:%M:%S.%f"))
    end_date = DateField(
        "End Date: ", 
        validators=[DataRequired()], 
        default = datetime.now())
    
    submit = SubmitField()

class SearchUser(FlaskForm):
    user_to_search = StringField()
    submit = SubmitField()