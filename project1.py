from flask import Flask,request,render_template,session,redirect
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "Sina1234"
app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/login",methods=["POST"])
def login():
    return render_template("loginform.html")

@app.route("/result", methods=["GET", "POST"])
def show_the_final_result():

    if request.method == "POST":
        username = request.form.get("username")
        userid = request.form.get("userid")

        session.permanent = True

        session["username"] = username
        session["userid"] = userid

    if "username" not in session or session["username"] is None:
        return redirect("/")

    return render_template(
        "result.html",
        username=session.get("username"),
        userid=session.get("userid")
    )


@app.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return redirect("/")
