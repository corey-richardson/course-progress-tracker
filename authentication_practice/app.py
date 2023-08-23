from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import RegistrationForm, LoginForm
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def load_user(user_id):
    # Replace this with actual loading logic from your JSON file
    with open('static/accounts.json', 'r') as file:
        users = json.load(file)["account list"]
        for user in users:
            if user['username'] == user_id:
                return User(user_id)

@app.route('/', methods=["GET","POST"])
def index():
    
    with open("static/accounts.json", "r") as acc:
        accounts = json.load(acc)["account list"]
    
    login = LoginForm()
    
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data
        
        for account in accounts:
            if account["username"] == username:
                
                if check_password_hash(account["password"], password):
                    user = User(username)
                    login_user(user)
                    return redirect(url_for("logged_in"))
                else:
                    print("bad password")
                    print(password)
                    print(account["password"])
    
    return render_template(
        "index.html",
        login = login
    )
    
# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    with open("static/accounts.json", "r") as acc:
        accounts = json.load(acc)
    
    register = RegistrationForm(csrf_enabled=False)

    if register.validate_on_submit():
        username = register.username.data
        password = generate_password_hash(register.password.data)
        
        new_user = {
            "username": f"{username}",
            "password": f"{password}"
        }
        
        accounts["account list"].append(new_user)
        with open("static/accounts.json", "w") as acc:
            json.dump(accounts, acc, indent = 4)
            
        register.update()
            
        return redirect(url_for("index"))

    return render_template(
        'register.html', 
        register=register)

@app.route('/logged_in', methods=['GET', 'POST'])
@login_required
def logged_in():
    
    return render_template(
        'logged_in.html',
        current_user = current_user)
    
@login_manager.unauthorized_handler
def unauthorized():
  # do stuff
  return "Sorry you must be logged in to view this page<br> Return to <a href='/'>Home</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))