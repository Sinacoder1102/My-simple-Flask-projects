# Importing models
from flask import Flask,request,session,render_template
from datetime import timedelta

# The main app
app = Flask(__name__)
app.secret_key = "Server's_reload245"
app.permanent_session_lifetime = timedelta(seconds=10)

@app.route("/")
def loginpage():
    return render_template("loginform01.html")

@app.route("/saving",methods=["POST"])
def show_it():
    username = request.form.get("username")
    password = request.form.get("password")
    user_id = request.form.get("userid")

    session.permanent = True

    session["username"] = username
    session["userid"] = user_id

    return render_template("deletelog.html" , message = "Your informations was saved succesfully!")

@app.route("/logout",methods=["POST"])
def log_out_user():
    session.clear()
    return "Your informations succesfully removed from on this page!"