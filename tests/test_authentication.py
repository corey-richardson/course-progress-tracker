# USAGE:
# pytest -v --no-header tests/test_authentication.py | tee tests/results.txt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from authenticate import (
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

def test_Registration_empty():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(csrf_token=csrf_token)
            assert not form.validate()
            assert form.errors
            
def test_Registration_valid():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="valid-username",
                password="ValidPassword1!",
                password2="ValidPassword1!",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_Registration_passwords_not_matching():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="valid-username",
                password="ValidPassword1!",
                password2="NonMatchingPassword1!",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            
def test_Registration_existing_username():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="TEST_ACCOUNT_DONT_DELETE",
                password="ValidPassword1!",
                password2="ValidPassword1!",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            
def test_Registration_space_in_username():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="Invalid username",
                password="ValidPassword1!",
                password2="ValidPassword1!",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors

def test_Registration_punc_in_username():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username=":Invalid@Username;",
                password="ValidPassword1!",
                password2="ValidPassword1!",
                csrf_token = csrf_token
            )
            assert not form.validate()
            assert form.errors
            
def test_Registration_allowed_punc_in_username():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="Valid-Username",
                password="ValidPassword1!",
                password2="ValidPassword1!",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_Registration_short_password():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="Sh0rt!",
                password2="Sh0rt!",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors
            
def test_Registration_no_lowercase_password():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="INVAL1DPASSW0RD!",
                password2="INVAL1DPASSW0RD!",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors
            
def test_Registration_no_uppercase_password():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="inval1dpassw0rd!",
                password2="inval1dpassw0rd!",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors
            
def test_Registration_no_punc_password():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="Inval1dPassw0rd",
                password2="Inval1dPassw0rd",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors

def test_Registration_space_in_password():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="Inval1d Passw0rd!",
                password2="Inval1d Passw0rd!",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors

def test_Registration_no_numbers():
    with app.test_request_context('/register'):
        with app.test_client() as client:
            response = client.get('/register')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = RegistrationForm(
                username="RESERVED_FOR_TESTING",
                password="InvalidPassword!",
                password2="InvalidPassword!",
                csrf_token = csrf_token
            )
            assert not form.validate_on_submit()
            assert form.errors
                        
def test_Login_valid():
    with app.test_request_context('/'):
        with app.test_client() as client:
            response = client.get('/')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = LoginForm(
                username="DONT_DELETE_ME_PLEASE",
                password="TestPassword!",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors

def test_Login_empty():
    with app.test_request_context('/'):
        with app.test_client() as client:
            response = client.get('/')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = LoginForm(csrf_token=csrf_token)
            assert not form.validate()
            assert form.errors
                      
def test_Login_valid():
    with app.test_request_context('/'):
        with app.test_client() as client:
            response = client.get('/')
            csrf_token = extract_csrf_token(response.data.decode("utf-8"))

            form = LoginForm(
                username="DONT_DELETE_ME_PLEASE",
                password="TestPassword!",
                csrf_token = csrf_token
            )
            assert form.validate()
            assert not form.errors
            
def test_protected_route():
    with app.test_client() as client:
        response = client.get('/homepage', follow_redirects=True)
        assert b'Sorry you must be logged in' in response.data