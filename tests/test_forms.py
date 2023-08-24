# USAGE:
# pytest -v --no-header tests/test_forms.py | tee tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User
from flask_login import current_user, login_user
from forms import (
    AddToLog, 
    DateRange, 
    ModuleCompleted,
)

import re
def extract_csrf_token(content):
    match = re.search(
        r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"', 
        content)
    if match:
        return match.group(1)
    return None

####################################################
# The following test cases test the form: AddToLog #
####################################################
        
def test_AddToLog_empty():
    '''
    Test an empty AddToLog form
    Expect the form to fail validation
    '''
    with app.test_request_context("/learning_log"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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

#####################################################
# The following test cases test the form: DateRange #
#####################################################

def test_DateRange_empty():
    '''
    Test an empty DateRange form
    Expect the form to fail validation
    '''
    with app.test_request_context("/learning_log"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
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
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/learning_log')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = DateRange(
                start_date = "2023-08-18 00:00:00",
                end_date = "",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            