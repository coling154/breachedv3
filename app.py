# App.py
# Author: Ryan Quirk <ryan.quirk6@protonmail.ch>
# Adapted By: Colin Gasiewicz
# Description: This is the main flask application. This script
# initializes the app, and handles all http requests & api calls.
from flask import Flask, request, render_template, redirect, flash
import sql_tools as sql
import hashlib
import re

app = Flask(__name__, static_folder="static")  # Static folder contains images + css file

# If this app was scaled and deployed, the secret key would need to be a 
# unique key preferably generated by some sort of cryptographic function (AES or SHA),
# stored as an environmental variable on the server. This key is needed for session handling
app.config['SECRET_KEY'] = "secretkey"


# Landing page for app
@app.route('/')
def index():
    return render_template("landing.html")  # Serve landing.html to user


# Handles the Check Password button which sends an
# HTTP POST request containing the input password
@app.route('/checkPass', methods=["POST"])
def checkPass():
    if request.method == "POST":

        # Send alert if form is empty
        if request.form['value'] == "":
            flash("ALERT: Please enter email or password", "noFill")
            return redirect("/")

        pwd = request.form['value']
        pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()  # Hash the password

        # Check whether the email is in the database, then redirect to according page
        con = sql.connect()
        if sql.checkPassword(pwd, con):
            flash("WARNING: Your password has been breached!", "danger")
            return redirect("/")

        else:
            flash("ALL GOOD: Your password has not been breached... live to fight another day", "good")
            return redirect("/")


# Handles the Check Email button which sends an
# HTTP POST request containing the input email
@app.route('/checkEmail', methods=["POST"])
def checkEmail():
    if request.method == 'POST':

        # Send alert if form is empty
        if request.form['value'] == "":
            flash("ALERT: Please enter email or password", "noFill")
            return redirect("/")

        email = request.form['value']

        # Use regex to validate if input is a proper email
        if not re.search(r".+@.+\..*", email):
            flash("ALERT: Please enter valid email", "noFill")
            return redirect("/")

        # Hash the email
        email = hashlib.sha256(email.encode('utf-8')).hexdigest()

        # Check whether the email is in the database, then redirect to according page
        con = sql.connect()
        if sql.checkEmail(email, con):
            flash("WARNING: Your email has been breached!", "danger")
            return redirect("/")
        else:
            flash("ALL GOOD: Your email has not been breached... live to fight another day", "good")
            return redirect("/")


if __name__ == '__main__':
    # Global is needed so the variable can be accessed within functions
    app.run(debug=True)
