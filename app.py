"""
Game Blog
"""

import os
import flask

app = flask.Flask(__name__)
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# app.secret_key = "thisissecretkey"


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/logout")
def logout():
    pass


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/account")
def account():
    pass


@app.route("/main")
def main():
    pass


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
