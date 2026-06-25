from flask import Flask, redirect,session,render_template,request,url_for

app = Flask(__name__)
app.secret_key = "sinazarei78952"

@app.route("/")
def loginindex():
    return render_template("form12.html")

@app.route("/login", methods=["GET", "POST"])
def mainindex():

    if request.method == "POST":
        username = request.form.get("username")
        userid = request.form.get("id")

        print("username =", username)
        print("userid =", userid)

        session["username"] = username
        session["userid"] = userid

        # print("session =", dict(session))

        return redirect(url_for("show"))

    return render_template("form.html")

@app.route("/situation",methods=["GET","POST"])
def show():
    if "username" not in session:
        return redirect(url_for("mainindex"))
    
    username = session["username"]
    userid = session["userid"]

    return f"Your username : {username} and your id : {userid}"

@app.route("/logout")
def user_logout():
    session.clear()

    return redirect(url_for("mainindex"))

