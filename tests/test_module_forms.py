# USAGE:
# pytest -v --no-header tests/test_forms.py | tee tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User
from flask_login import login_user
from forms import (
    AddModule, 
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

#####################################################
# The following test cases test the form: AddModule #
#####################################################

def test_AddModule_empty():
    '''
    Test an empty AddModule form
    Expect the form to fail validation
    '''
    with app.test_request_context("/add_module"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
        form = AddModule()
        assert not form.validate()
        assert form.errors

def test_AddModule_valid():
    '''
    Test a valid AddModule form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_module'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_module')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddModule(
                name = "Test Title",
                desc = "This test ensures the form accepts valid input.",
                code = "TEST001",
                year = "First",
                optional = "true",
                completed = "true",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_AddModule_invalid():
    '''
    Test an invalid AddModule form
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_module'):
        with app.test_client() as client:      
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_module')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = AddModule(
                name = "Test Title",
                desc = "This test ensures the form denies invalid input.",
                code = "TEST001",
                year = "1st",
                optional = "yarp",
                completed = "narp",
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
    with app.test_request_context("/add_module"):
        login_user(User('TEST_ACCOUNT_DONT_DELETE'))
        form = ModuleCompleted()
        assert not form.validate()
        assert form.errors
      
# ENSURE "Test Module" IS IN THE MODULE LIST BEFORE TESTING           
def test_ModuleCompleted_valid():
    '''
    Test a valid ModuleCompleted form
    Expect the form to pass validation
    '''
    with app.test_request_context('/add_module'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_module')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = ModuleCompleted(
                status = "true",
                completed = "Test Module",
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
    with app.test_request_context('/add_module'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_module')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))       
                        
            form = ModuleCompleted(
                status = "false",
                completed = "Learn Skydiving for Beginners",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
        
def test_ModuleCompleted_missing_required_field():
    '''
    Test a ModuleCompleted form with missing required fields
    Expect the form to fail validation
    '''
    with app.test_request_context('/add_module'):
        with app.test_client() as client:
            login_user(User('TEST_ACCOUNT_DONT_DELETE'))
            response = client.get('/add_module')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))
             
            form = ModuleCompleted(
                status = "true",
                completed = "",
                csrf_token=csrf_token
            )
            assert not form.validate()
            assert 'completed' in form.errors
