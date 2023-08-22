from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField)

from wtforms.validators import DataRequired, ValidationError, EqualTo
import json
import string

class RegistrationForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.update() 
        
    def update(self):
        with open("static/accounts.json", "r") as acc:
            self.users = json.load(acc)["account list"]
        
        
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField(
        "Password", 
        validators=[DataRequired()])
    
    password2 = PasswordField(
        "Repeat Password", 
        validators=[DataRequired(), 
                    EqualTo('password')])
    
    def validate_username(self, username):
        username = username.data
        if " " in username:
            self.username.errors.append("Bad username: No spaces!")
            raise ValidationError('Illegal character in username')
        for user in self.users:
            if user['username'] == username:
                self.username.errors.append("Username already taken")
                raise ValidationError('This username is already taken. Please choose a different one.')

    def strength_test_password(self, password):
        password = password.data
        if " " in password:
            self.username.errors.append("No spaces!")
            raise ValidationError('Bad password: No spaces!')
        if len(password) < 8:
            self.username.errors.append("Length")
            raise ValidationError("Bad password: Length!")
        if not any(char in string.ascii_lowercase for char in password):
            self.username.errors.append("No Lowercase")
            raise ValidationError("Bad password: No Lowercase!")
        if not any(char in string.ascii_uppercase for char in password):
            self.username.errors.append("No Uppercase")
            raise ValidationError("Bad password: No Uppercase!")
        if not any(char in string.punctuation for char in password):
            self.username.errors.append("No Punctuation")
            raise ValidationError("Bad password: No Punctuation!")
            
    def validate_on_submit(self):
        if not super().validate():
            return False
        
        try:
            self.validate_username(self.username)
        except ValidationError:
            self.username.errors.append("Username already exists")
            return False
            
        try:
            self.strength_test_password(self.password)
        except ValidationError:
            self.username.errors.append("Password does not meet strength requirements")
            return False

        return True
    
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField(
        "Password", 
        validators=[DataRequired()])
    
    submit = SubmitField("Login")