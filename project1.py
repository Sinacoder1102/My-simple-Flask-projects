# Importing models
from flask import Flask,request,redirect,render_template, session,url_for,flash
import psycopg
from datetime import timedelta
from werkzeug.security import generate_password_hash,check_password_hash

# Doing initial settings
app = Flask(__name__)
app.secret_key = "Sinasecret123"
app.permanent_session_lifetime = timedelta(minutes=2)

# Connecting to postgres
def connection():
    return psycopg.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="21200",
        port=5432
    )

# Main route
@app.route("/")
def red_to_login():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("loginform.html")

@app.route("/register" , methods=["POST"])
def register():
    return render_template("registerform.html")

@app.route("/savinginfs",methods=["POST"])
def saving_informations():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        userid = request.form.get("userid")

        session["username"] = username
        session["userid"] = userid

        session.permanent = True

        secpassword = generate_password_hash(password)

        conn = connection()
        postcur = conn.cursor()

        postcur.execute(
            "INSERT INTO siteusers(username,password,userid) VALUES(%s,%s,%s)",
            (username,secpassword,userid,)
        )

        conn.commit()
        postcur.close()
        conn.close()

        return redirect(url_for("login"))
    
    except Exception as ex:
        return f"Ops!!!!!!! : {ex}"
    
@app.route("/welcomeback",methods=["POST"])
def saywelcomeback():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = connection()
    postcurs = conn.cursor()

    postcurs.execute(
        "SELECT username,password,userid FROM siteusers WHERE username = %s",
        (username,)
    )

    user = postcurs.fetchone()

    postcurs.close()
    conn.close()

    if user is None:
        return "User not found!"
    
    db_username, db_pass, db_userid = user

    if check_password_hash(db_pass,password):
        session["username"] = db_username
        session["userid"] = db_userid
        session.permanent = True

        return redirect(url_for("dashboard"))
    else:
        return "<h1>Wrong password!!!!</h1>"
    
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    
    return render_template(
        "dashboard.html",
        username = session["username"],
        userid = session["userid"]
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def showprof():
    if "username" not in session:
        return redirect(url_for("login"))
    
    return render_template(
        "profile.html",
        username = session["username"],
        userid = session["userid"]
    )

@app.route("/editprofile")
def editprof():
    if "username" not in session:
        return redirect(url_for("login"))
    
    return render_template(
        "editprofile.html",
        username = session["username"]
    )

@app.route("/updateprofile" , methods=["POST"])
def updateprof():
    if "username" not in session:
        return redirect(url_for("login"))
    
    new_username = request.form.get("username")
    
    conn = connection()
    postcursor = conn.cursor()

    postcursor.execute(
        """UPDATE siteusers
        SET username = %s
        WHERE userid = %s
        """,
        (new_username,session["userid"])
    )

    conn.commit()
    postcursor.close()
    conn.close()

    session["username"] = new_username

    return redirect(url_for("showprof"))

@app.route("/changepassword")
def changepassword():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("changepass.html")


@app.route("/updatepassword" , methods=["POST"])
def updatepass():
    if "username" not in session:
        return redirect(url_for("login"))

    new_pass = request.form.get("newpassword")
    old_pass = request.form.get("oldpassword")

    conn = connection()
    cur2 = conn.cursor()

    cur2.execute(
        "SELECT password FROM siteusers WHERE userid = %s",
        (session["userid"],)
    )

    user = cur2.fetchone()

    db_password = user[0]
    
    if check_password_hash(db_password,old_pass):
       new_hashed_password = generate_password_hash(new_pass)
       cur2.execute(
           """
           UPDATE siteusers
           SET password = %s
           WHERE userid = %s
           """,
           (new_hashed_password,session["userid"])
       ) 

       conn.commit()
       cur2.close()
       conn.close()

       return redirect(url_for("showprof"))
    
    else:
        cur2.close()
        conn.close()
        return "Current password is incorrect!"
    
