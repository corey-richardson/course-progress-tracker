# USAGE:
# pytest -v tests/test_forms.py > tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from forms import AddCourse, AddToLog, CourseCompleted, ModuleCompleted

import re
def extract_csrf_token(content):
    match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', content)
    if match:
        return match.group(1)
    return None

#################################################################################
# The following tests ensure that an error is raised if the form is left empty. #
# This checks the DataRequired() validators present on most fields.             #
#################################################################################

def test_AddCourse_empty():
    with app.test_request_context("/add"):
        form = AddCourse()
        assert not form.validate()
        assert form.errors

def test_CourseCompleted_empty():
    with app.test_request_context("/add"):
        form = CourseCompleted()
        assert not form.validate()
        assert form.errors
        
def test_ModuleCompleted_empty():
    with app.test_request_context("/add"):
        form = ModuleCompleted()
        assert not form.validate()
        assert form.errors
        
def test_AddToLog_empty():
    with app.test_request_context("/learning_log"):
        form = AddToLog()
        assert not form.validate()
        assert form.errors

##############################################################################
# The following tests ensure that the forms successfully validate when valid #
# input data is submitted.                                                   #
##############################################################################

def test_AddCourse_valid():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddCourse(
                name = "Test Title",
                desc = "This test ensures the Form accepts valid input.",
                url = "https://docs.pytest.org/en/7.4.x",
                provider = "Pytest Academy",
                length = "1 minute",
                section = "Pytest",
                completed = "true",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors

# ENSURE "Learn Python 3" IS IN THE COURSE LIST BEFORE TESTING           
def test_CourseCompleted_valid():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = CourseCompleted(
                status = "true",
                completed_course = "Learn Python 3",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors

# ENSURE "Learn Skydiving for Beginners" IS *NOT* IN THE COURSE LIST BEFORE TESTING            
def test_CourseCompleted_invalid():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = CourseCompleted(
                status = "false",
                completed_course = "Learn Skydiving for Beginners",
                csrf_token = csrf_token
            )

            assert not form.validate()
            assert form.errors
            
# ENSURE "Software Engineering 1" IS IN THE MODULE LIST BEFORE TESTING           
def test_ModuleCompleted_valid():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = ModuleCompleted(
                status = "true",
                completed_module = "Software Engineering 1",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors

# ENSURE "Learn Skydiving for Beginners" IS *NOT* IN THE MODULE LIST BEFORE TESTING            
def test_ModuleCompleted_invalid():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = ModuleCompleted(
                status = "false",
                completed_module = "Learn Skydiving for Beginners",
                csrf_token = csrf_token
            )

            assert not form.validate()
            assert form.errors

def test_AddToLog_valid():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = AddToLog(
                title="Test Post Title",
                topics="Test Post Topics",
                body="Lorum Ipsum blah blah blah",
                link_title="Pytest Documentation",
                link="https://docs.pytest.org/en/7.4.x/",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors
            
def test_AddToLog_valid_optional_fields():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = AddToLog(
                title="Test Post Title",
                topics="Test Post Topics",
                body="Lorum Ipsum blah blah blah",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors
            

###########################################################################
# The following tests ensure that the form don't validate when a required #
# field is missing.                                                       #
###########################################################################

def test__AddToLog_required_fields():
    with app.test_request_context('/'):
        form = AddToLog(
            title="Test Title",
            topics="",
            body="Test Body",
        )
        assert not form.validate()
        assert 'topics' in form.errors
        
def test_CourseCompleted_required_fields():
    with app.test_request_context('/'):
        form = CourseCompleted(
            status = "true",
            completed_course = ""
        )
        assert not form.validate()
        assert 'completed_course' in form.errors
        
def test_ModuleCompleted_required_fields():
    with app.test_request_context('/'):
        form = ModuleCompleted(
            status = "true",
            completed_module = ""
        )
        assert not form.validate()
        assert 'completed_module' in form.errors
        
def test_AddToLog_required_fields():
    with app.test_request_context('/'):
        form = AddToLog(
            title="Test Post Title",
            topics="",
            body="Lorum Ipsum blah blah blah"
        )
        assert not form.validate()
        assert 'topics' in form.errors