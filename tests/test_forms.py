# USAGE:
# pytest -v --no-header tests/test_forms.py | tee tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User
from flask_login import current_user, login_user
from forms import (
    AddCourse, 
    AddToLog, 
    CourseCompleted, 
    DateRange, 
    ModuleCompleted,
    RegistrationForm,
    LoginForm,
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
    with app.test_request_context("/add"):
        login_user(User('test_user'))
        form = AddCourse()
        assert not form.validate()
        assert form.errors

def test_AddCourse_valid():
    '''
    Test a valid AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddCourse(
                name = "Test Title",
                desc = "This test ensures the form accepts valid input.",
                url = "https://docs.pytest.org/en/7.4.x",
                provider = "Pytest Academy",
                length = "1 minute",
                section = "Pytest",
                completed = "true",
                owner = "Test Owner",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_AddCourse_invalid():
    '''
    Test an invalid AddCourse form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:      
            login_user(User('test_user'))
            response = client.get('/add')
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

####################################################
# The following test cases test the form: AddToLog #
####################################################
        
def test_AddToLog_empty():
    '''
    Test an empty AddToLog form
    Expect the form to fail validation
    '''
    with app.test_request_context("/learning_log"):
        login_user(User('test_user'))
        form = AddToLog()
        assert not form.validate()
        assert form.errors
        
def test_AddToLog_valid():
    '''
    Test a valid AddToLog form
    Expect the form to pass validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test a AddToLog form with missing required fields
    Expect the form to fail validation, listing 'topics' in the form errors
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test a valid AddToLog form missing optional fields
    Expect the form to pass validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test an invalid AddToLog form where 'link' is set but 'link_title'
    is not; mutually inclusive events.
    Expect the form to fail validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test an invalid AddToLog form where 'link_title' is set but 'link'
    is not; mutually inclusive events.
    Expect the form to fail validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test an empty CourseCompleted form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add"):
        login_user(User('test_user'))
        form = CourseCompleted()
        assert not form.validate()
        assert form.errors

# ENSURE "Learn Python 3" IS IN THE COURSE LIST BEFORE TESTING           
def test_CourseCompleted_valid():
    '''
    Test a valid CourseCompleted form
    Expect the form to pass validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = CourseCompleted(
                status = "true",
                completed_course = "Learn Python 3",
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
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test a CourseCompleted form with missing required fields
    Expect the form to fail validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test an empty DateRange form
    Expect the form to fail validation
    '''
    with app.test_request_context("/learning_log"):
        login_user(User('test_user'))
        form = DateRange()
        assert not form.validate()
        assert form.errors

def test_DateRange_valid():
    '''
    Test a valid DateRange form
    Expect the form to pass validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "2023-08-18 00:00:00",
                end_date = "2023-08-21 23:59:59.999999",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_DateRange_missing_required_field():
    '''
    Test a DateRange form with mising required fields
    Expect the form to fail validation
    '''
    with app.test_request_context('/learning_log'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "2023-08-18 00:00:00",
                end_date = "",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            
###########################################################
# The following test cases test the form: ModuleCompleted #
###########################################################

def test_ModuleCompleted_empty():
    '''
    Test an empty ModuleCompleted form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add"):
        login_user(User('test_user'))
        form = ModuleCompleted()
        assert not form.validate()
        assert form.errors
      
# ENSURE "Software Engineering 1" IS IN THE MODULE LIST BEFORE TESTING           
def test_ModuleCompleted_valid():
    '''
    Test a valid ModuleCompleted form
    Expect the form to pass validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = ModuleCompleted(
                status = "true",
                completed_module = "Software Engineering 1",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors

# ENSURE "Learn Skydiving for Beginners" IS *NOT* IN THE 
# MODULE LIST BEFORE TESTING            
def test_ModuleCompleted_invalid():
    '''
    Test an invalid ModuleCompleted form; 'Learn Skydiving for Beginners' is
    not a valid choice
    Expect the form to fail validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
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
    '''
    Test a ModuleCompleted form with missing required fields
    Expect the form to fail validation
    '''
    with app.test_request_context('/add'):
        with app.test_client() as client:
            login_user(User('test_user'))
            response = client.get('/add')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))
             
            form = ModuleCompleted(
                status = "true",
                completed_module = "",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'completed_module' in form.errors
        
