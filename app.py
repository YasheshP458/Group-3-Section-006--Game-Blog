# pylint: disable=invalid-envvar-default, unused-import, pointless-string-statement, no-member, invalid-name

"""
Game Blog

Nathan Heckman, Ba Choi, Yashesh Patel, 
Chris English, Aaron Reyes
"""

import os
from re import L
import flask
import requests
import bcrypt
from dotenv import load_dotenv, find_dotenv

from flask import Flask, session, abort, redirect

from flask_sqlalchemy import SQLAlchemy

from igdb import search_game_data, get_cover_url, clean_string, get_game_data

from oauth2client.contrib.flask_util import UserOAuth2
import google.oauth2.credentials
import google_auth_oauthlib.flow
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

# from flask_bcrypt import Bcrypt


from flask_login import (
    UserMixin,
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)

load_dotenv(find_dotenv())


app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["BCRYPT_LEVEL"] = 10
# bcrypt = Bcrypt(app)

# Point SQLAlchemy to your Heroku database
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["GOOGLE_OAUTH2_CLIENT_SECRETS_FILE"] = "client_secret.json"
# Point SQLAlchemy to Heroku database. Already accounted for postgres -> postgresql
app.config["SQLALCHEMY_DATABASE_URI"] = uri

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect(flask.url_for("login"))


class Users(db.Model, UserMixin):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.LargeBinary(), nullable=False)


db.create_all()
oauth2 = UserOAuth2(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if oauth2.has_credentials():
        return flask.render_template(
            "main.html", username=oauth2.email, user_id=oauth2.user_id
        )
    elif flask.request.method == "POST":
        user_form = flask.request.form
        user_name = user_form["userName"]
        userPW = user_form["userPW"]
        user = Users.query.filter_by(username=user_name).first()
        print(user.password)
        print(userPW)
        print(type(userPW))
        print(userPW.encode())
        userPW_hash = bcrypt.checkpw(userPW.encode("utf-8"), user.password)

        if userPW_hash:
            login_user(user)

            return flask.render_template("main.html", username=user.username)
        else:
            flask.flash("Can't Find User Info, Please Check Again")
            return flask.render_template("login.html")

    else:
        return flask.render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "POST":
        user_form = flask.request.form
        user_name = user_form["userName"]
        user_pw = user_form["userPW"]
        user_repw = user_form["userRePW"]
        isUN = Users.query.filter_by(username=user_form["userName"]).first()

        if not (user_name or user_pw or user_repw):
            flask.flash("All Blanks Must be Filled")
            return flask.redirect(flask.url_for("signup"))

        elif isUN:
            t = "The user name '"
            y = "' is already used"
            flask.flash(t + user_name + y)  # already exist
            return flask.redirect(flask.url_for("signup"))

        elif len(user_pw) < 4:
            flask.flash("Password Must be at least 4 digits")  # already exist
            return flask.redirect(flask.url_for("signup"))

        elif user_pw != user_repw:
            flask.flash(" Password Not Matching ")
            return flask.redirect(flask.url_for("signup"))

        else:
            user_pw_hash = bcrypt.hashpw(user_pw.encode("utf-8"), bcrypt.gensalt())
            user = Users(username=user_name, password=user_pw_hash)

            db.session.add(user)

            db.session.commit()
            x = "Sign Up Completed! Login with "
            flask.flash(x + user_name)
            return flask.redirect(flask.url_for("login"))
    return flask.render_template("signup.html")


# return flask.render_template("signup.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return flask.redirect(flask.url_for("index"))


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/account")
def account():
    pass


@app.route("/main", methods=["GET", "POST"])
def main():
    data = flask.request.form
    input_game = data["game"]
    if flask.request.method == "POST":
        if search_game_data(input_game) == "Invalid Name":
            flask.flash("Game does not exist or invalid name. Try again!")
        else:
            game_name, cover_url, game_summary = search_game_data(input_game)
            return flask.render_template(
                "main.html",
                game_name = game_name,
                cover_url = cover_url,
                game_summary = game_summary,
                username=oauth2.email,
                user_id=oauth2.user_id,
            )
    return flask.render_template(
        "main.html",
        username=oauth2.email,
        user_id=oauth2.user_id,
    )


@app.route("/oauth2authorize")
def oauth2authorize():
    pass


@app.route("/oauth2callback")
def oauth2callback():
    pass


# app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
app.run(debug=True)
