from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired
import json

COURSE_FILE_PATH = "static/courses.json"
MODULE_FILE_PATH = "static/modules.json"

class AddCourse(FlaskForm):
    name = StringField("Course Name: ", validators=[DataRequired()])
    desc = TextAreaField("Course Description: ", validators=[DataRequired()])
    url = URLField("Course Link: ", validators=[DataRequired()])
    provider = StringField("Course Provider: ", validators=[DataRequired()])
    length = StringField("Course Duration: ", validators=[DataRequired()])
    section = StringField("Topic: ", validators=[DataRequired()])  
    completed = SelectField(
        "Have you completed this course? ", 
        choices=[("true","Yes"),("false","No")], default="false")
    
    submit = SubmitField()
    
class CourseCompleted(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(CourseCompleted, self).__init__(*args, **kwargs)
        self.update_course_choices() 
    def update_course_choices(self):
        with open(COURSE_FILE_PATH, "r") as j:
            courses = json.load(j)["course list"]   
        choices_list = [course["name"] for course in courses]
        self.completed_course.choices = sorted(choices_list)
        
    status = SelectField("Status: ",
                         choices=[("true","finished"),("false","unfinished")],
                         validators=[DataRequired()])
    completed_course = SelectField(
        "Mark Course as Completed:", 
        validators=[DataRequired()])
    
    submit = SubmitField()
    
class ModuleCompleted(FlaskForm):
    with open(MODULE_FILE_PATH, "r") as j:
        modules = json.load(j)["module list"]    
    choices_list = [module["name"] for module in modules]
    status = SelectField(
        "Status: ",
        choices=[("true","finished"),("false","unfinished")],
        validators=[DataRequired()])
    completed_module = SelectField(
        "Mark Course as Completed:", 
        choices=choices_list,
        validators=[DataRequired()])
    submit = SubmitField()
    
class AddToLog(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()])
    topics = StringField("Topics Covered: ", validators=[DataRequired()])
    body = TextAreaField("Post Contents: ", validators=[DataRequired()])
    link_title = StringField("Link Title: ")
    link = URLField("Relevant Link: ")
    submit = SubmitField()