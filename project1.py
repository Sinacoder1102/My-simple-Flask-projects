from flask import Flask, redirect,request,render_template,session,make_response

app = Flask(__name__)
app.secret_key = "mysecret9865"

@app.route("/")
def index():
    return render_template("form12.html")

@app.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        user_id = request.form.get("userid")
        password = request.form.get("password")

        if username == "admin" and password == "4567":
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/result")
        else:
            return "<h1>wrong username or password for admin</h1>"
    if request.method == "GET":
        return redirect("/")

@app.route("/result",methods=["POST"])
def check():
    if "username" not in session:
        return redirect("/")
    return render_template("result.html",username1 = session.get("username"),user_id1 = session.get("user_id"))