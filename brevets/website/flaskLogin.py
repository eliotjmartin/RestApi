"""
Flask-Login and Flask-WTF example
"""
from urllib.parse import urlparse, urljoin
from flask import Flask, request, render_template, redirect, url_for, flash, abort, session
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user, UserMixin,
                         confirm_login, fresh_login_required)
from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, StringField, validators, PasswordField
import requests
from passlib.hash import sha256_crypt as pwd_context
import json


class LoginForm(Form):
    username = StringField('Username', [
        validators.Length(min=2, max=25,
                          message=u"Huh? Little too short for a username."),
        validators.InputRequired(u"Forget something?")])
    password = PasswordField("Password", [
        validators.Length(min=2, max=25, message=u"Huh? Little too short for a password."),
        validators.InputRequired(u"Forget something?")])
    remember = BooleanField('Remember me')

class RegistrationForm(Form):
    username = StringField('Username', [
        validators.Length(min=2, max=25,
                          message=u"Huh, little too short for a username."),
        validators.InputRequired(u"Forget something?")])
    remember = BooleanField('Remember me')
    password = PasswordField("Password", [
        validators.Length(min=2, max=25, message=u"Huh? Little too short for a password."),
        validators.InputRequired(u"Forget something?"), 
        validators.EqualTo('verification', message='Passwords must match')])
    verification = PasswordField("Verify Password")
    

def is_safe_url(target):
    """
    :source: https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.token = ''

    # set token method?
    def set_token(self, token):
        self.token = token
        return self



app = Flask(__name__)
app.secret_key = "and the cats in the cradle and the silver spoon"

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.session_protection = "strong"

login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."

login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, session['username']).set_token(session['token'])


login_manager.init_app(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

###
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
        password = pwd_context.using(rounds=1122,salt='123hello').encrypt(password)
        u = requests.post(f'http://restapi:5000/register?username={username}&password={password}').json()
        if u['message'] == 'Success':
            flash(u"Success! Now try logging in")
            return redirect(url_for('login'))
        flash(u"User already exists in the database! Try picking a more unique username")
    return render_template("register.html", form=form)

@app.route("/secret")
@login_required
def secret():
    return render_template('secret.html')

@app.route('/everything')
@login_required
def everything():
    token = current_user.token
    k = request.args.get("k", type=int) or -1
    csv = request.args.get("csv", type=str)
    app.logger.debug("k = {}".format(k))
    app.logger.debug("csv= {}".format(csv))
    if csv == None:
        r = requests.get(f'http://restapi:5000/listAll?top={k}&token={token}')
    else:
        r = requests.get(f'http://restapi:5000/listAll/csv?top={k}&token={token}')
    return r.text

@app.route('/open')
@login_required
def open():
    token = current_user.token
    k = request.args.get("k", type=int) or -1
    csv = request.args.get("csv", type=str)
    if csv == None:
        r = requests.get(f'http://restapi:5000/listOpenOnly?top={k}&token={token}')
    else:
        r = requests.get(f'http://restapi:5000/listOpenOnly/csv?top={k}&token={token}')
    return r.text

@app.route('/close')
@login_required
def close():
    token = current_user.token
    k = request.args.get("k", type=int) or -1
    csv = request.args.get("csv", type=str)
    if csv == None:
        r = requests.get(f'http://restapi:5000/listCloseOnly?top={k}&token={token}')
    else:
        r = requests.get(f'http://restapi:5000/listCloseOnly/csv?top={k}&token={token}')
    return r.text

###

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        password = pwd_context.using(rounds=1122,salt='123hello').encrypt(password)
        token = requests.get(f'http://restapi:5000/token?username={username}&password={password}').json()
        app.logger.debug(f'RESPONSE***  {token}')
        if not token['response']=='Failure':  # pwd_context.verify(password, hashed)
            remember = request.form.get("remember", "false") == "true"
            session["token"] = token['token']
            session["username"] = username 
            user = User(token['id'], session['username']).set_token(session['token'])
            if login_user(user, remember=remember):
                flash("Logged in!")
                flash("I'll remember you") if remember else None
                next = request.args.get("next")
                if not is_safe_url(next):
                    abort(400)
                return redirect(next or url_for('index'))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username or password.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
