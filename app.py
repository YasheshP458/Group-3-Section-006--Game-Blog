# pylint: disable=invalid-envvar-default, unused-import, pointless-string-statement

"""
Game Blog

Nathan Heckman, Ba Choi, Yashesh Patel, 
Chris English, Aaron Reyes
"""

import os
import flask
import requests

from flask import Flask, session, abort, redirect

from flask_sqlalchemy import SQLAlchemy

from oauth2client.contrib.flask_util import UserOAuth2
import google.oauth2.credentials
import google_auth_oauthlib.flow

app = flask.Flask(__name__)
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

''' 
USED FOR CLEANING DATABASE URI, NEED TO TOUCH UP

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
'''

app.config["SECRET_KEY"] = "thisissecretkey"
app.config["GOOGLE_OAUTH2_CLIENT_SECRETS_FILE"] = "client_secret.json"
# Point SQLAlchemy to Heroku database. Already accounted for postgres -> postgresql
# app.config["SQLALCHEMY_DATABASE_URI"] = uri
# Gets rid of meaningless warnings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Database(db.Model):
    """Movie Data Database"""
    
    '''NEED TO CHANGE THIS. SKELETON CODE'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())

oauth2 = UserOAuth2(app)

@app.route("/login")
def login():
    if oauth2.has_credentials():
        return flask.render_template(
            "main.html", email=oauth2.email, user_id=oauth2.user_id
        )
    else:
        return flask.render_template("login.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


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


@app.route("/main")
def main():
    return flask.render_template("main.html")


@app.route("/oauth2authorize")
def oauth2authorize():
    pass


@app.route("/oauth2callback")
def oauth2callback():
    pass


# app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
app.run(debug=True)
