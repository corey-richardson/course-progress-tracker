# USAGE:
# pytest -v tests/test_forms.py > tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from forms import AddCourse, AddToLog, CourseCompleted, DateRange, ModuleCompleted
from wtforms.validators import ValidationError
import pytest

import re
def extract_csrf_token(content):
    match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', content)
    if match:
        return match.group(1)
    return None

#################################################################################
# The following tests ensure that an error is raised if the form is left empty. #
# This checks the DataRequired() validators present on most fields.             #
#                                                                               #
# The following tests ensure that the forms successfully validate when valid    #
# input data is submitted.                                                      #
#                                                                               #
# The following tests ensure that the form doesn't validate when a required     #
# field is missing.                                                             #
#                                                                               #
# The following tests ensure that the form don't validate either both or        #
# neither of 'link' and 'link_title' are set.                                   #
# link and link_title OR not link and not link_title                            # 
#################################################################################

#####################################################
# The following test cases test the form: AddCourse #
#####################################################

def test_AddCourse_empty():
    with app.test_request_context("/add"):
        form = AddCourse()
        assert not form.validate()
        assert form.errors

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

####################################################
# The following test cases test the form: AddToLog #
####################################################
        
def test_AddToLog_empty():
    with app.test_request_context("/learning_log"):
        form = AddToLog()
        assert not form.validate()
        assert form.errors
        
def test_AddToLog_valid():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = AddToLog(
                title="Test Post Title",
                project="Test Project",
                topics="Test Post Topics",
                body="Lorum Ipsum blah blah blah",
                link_title="Pytest Documentation",
                link="https://docs.pytest.org/en/7.4.x/",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors

def test_AddToLog_missing_required_field():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))
                
            form = AddToLog(
                title="Test Title",
                project="Test Project",
                topics="",
                body="Test Body",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'topics' in form.errors 

def test_AddToLog_valid_missing_optional_fields():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = AddToLog(
                title="Test Post Title",
                project="Test Project",
                topics="Test Post Topics",
                body="Lorum Ipsum blah blah blah",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors

# 'link' set but not 'link_title'           
def test_AddToLog_only_link():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8")) 
            form = AddToLog(
                title="Test Post Title",
                project="Test Project",
                topics="Pytest",
                body="Lorum Ipsum blah blah blah",
                link="https://docs.pytest.org/en/7.4.x/",
                csrf_token=csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors

# 'link_title' set but not 'link'     
def test_AddToLog_only_link_title():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8")) 
            form = AddToLog(
                title="Test Post Title",
                project="Test Project",
                topics="Pytest",
                body="Lorum Ipsum blah blah blah",
                link_title="Test Link Title",
                csrf_token=csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors
                
###########################################################
# The following test cases test the form: CourseCompleted #
###########################################################
                                      
def test_CourseCompleted_empty():
    with app.test_request_context("/add"):
        form = CourseCompleted()
        assert not form.validate()
        assert form.errors

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

def test_CourseCompleted_misssing_required_field():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8")) 
            
            form = CourseCompleted(
                status = "true",
                completed_course = "",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'completed_course' in form.errors                       

#####################################################
# The following test cases test the form: DateRange #
#####################################################

def test_DateRange_empty():
    with app.test_request_context("/learning_log"):
        form = DateRange()
        assert not form.validate()
        assert form.errors

def test_DateRange_valid():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "2023-08-18 00:00:00",
                end_date = "2023-08-21 23:59:59.999999",
                csrf_token = csrf_token
            )

            assert form.validate()
            assert not form.errors
            
def test_DateRange_missing_start_required_field():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "2023-08-18 00:00:00",
                end_date = "",
                csrf_token = csrf_token
            )

            assert not form.validate()
            assert form.errors
            
def test_DateRange_missing_end_required_field():
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "",
                end_date = "2023-08-21 23:59:59.999999",
                csrf_token = csrf_token
            )

            assert not form.validate()
            assert form.errors
            
###########################################################
# The following test cases test the form: ModuleCompleted #
###########################################################

def test_ModuleCompleted_empty():
    with app.test_request_context("/add"):
        form = ModuleCompleted()
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
        
def test_ModuleCompleted_missing_required_field():
    with app.test_request_context('/add'):
        with app.test_client() as client:
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))
             
            form = ModuleCompleted(
                status = "true",
                completed_module = "",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'completed_module' in form.errors
        