# USAGE:
# pytest -v --no-header tests/test_forms.py | tee tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User
from flask_login import login_user
from forms import (
    AddCourse, 
    CourseCompleted, 
)

import re
def extract_csrf_token(content):
    match = re.search(
        r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', 
        content)
    if match:
        return match.group(1)
    return None

#####################################################
# The following test cases test the form: AddCourse #
#####################################################

def test_AddCourse_empty():
    '''
    Test an empty AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add_course"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
        form = AddCourse()
        assert not form.validate()
        assert form.errors

def test_AddCourse_valid():
    '''
    Test a valid AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_course'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_course')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddCourse(
                name = "Test Title",
                desc = "This test ensures the form accepts valid input.",
                url = "https://docs.pytest.org/en/7.4.x",
                provider = "Pytest Academy",
                length = "1 minute",
                section = "Pytest",
                completed = "true",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_AddCourse_invalid():
    '''
    Test an invalid AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_course'):
        with app.test_client() as client:      
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_course')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddCourse(
                name = "Test Title",
                desc = "This test ensures the form denies invalid input.",
                url = "https://docs.pytest.org/en/7.4.x",
                provider = "Pytest Academy",
                length = "1 minute",
                section = "Pytest",
                completed = "im an invalid choice",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            
###########################################################
# The following test cases test the form: CourseCompleted #
###########################################################
                                      
def test_CourseCompleted_empty():
    '''
    Test an empty CourseCompleted form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add_course"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
        form = CourseCompleted()
        assert not form.validate()
        assert form.errors

# ENSURE "Test Course" IS IN THE COURSE LIST BEFORE TESTING           
def test_CourseCompleted_valid():
    '''
    Test a valid CourseCompleted form
    Expect the form to pass validation
    '''
    with app.test_request_context('/add_course'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_course')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = CourseCompleted(
                status = "true",
                completed = "Test Course",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors

# ENSURE "Learn Skydiving for Beginners" IS *NOT* IN THE 
# COURSE LIST BEFORE TESTING            
def test_CourseCompleted_invalid():
    '''
    Test an invalid CourseCompleted form; 'Learn Skydiving for Beginners' is
    not a valid choice
    Expect the form to fail validation 
    '''
    with app.test_request_context('/add_course'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_course')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = CourseCompleted(
                status = "false",
                completed = "Learn Skydiving for Beginners",
                csrf_token = csrf_token
            )

            assert not form.validate()
            assert form.errors

def test_CourseCompleted_misssing_required_field():
    '''
    Test a CourseCompleted form with missing required fields
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_course'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_course')
            csrf_token = extract_csrf_token(response.data.decode("utf-8")) 
            
            form = CourseCompleted(
                status = "true",
                completed = "",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'completed' in form.errors            