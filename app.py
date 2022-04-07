# pylint: disable=invalid-envvar-default

"""
Game Blog
"""

import os
import flask
import requests

from flask import Flask, session, abort, redirect

from oauth2client.contrib.flask_util import UserOAuth2
import google.oauth2.credentials
import google_auth_oauthlib.flow


app = flask.Flask(__name__)
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

app.config["SECRET_KEY"] = "thisissecretkey"
app.config["GOOGLE_OAUTH2_CLIENT_SECRETS_FILE"] = "client_secret.json"

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
