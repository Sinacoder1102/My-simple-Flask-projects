# Importing models
import re
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

@app.route("/register")
def register():
    return render_template("registerform.html")

@app.route("/savinginfs",methods=["POST"])
def saving_informations():
    try:
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        userid = request.form.get("userid","").strip()
        confirmpass = request.form.get("confirmpass" , "").strip()

        if password != confirmpass :
            flash("passwords are not match")
            return redirect(url_for("register"))

        conn = connection()
        postcur = conn.cursor()

        if not username or not password or not userid :
            flash("The informations required")
            return redirect(url_for("register"))

        if len(username) < 3 :
            flash("The username must be at least 3 characters")
            return redirect(url_for("register"))
        
        if len(username) > 20 :
            flash("The username mustn't be more than 20 characters")
            return redirect(url_for("register"))
        
        if not re.fullmatch(r"[A-Za-Z0--9_]+" , username):
            flash("Username only contains letter,numbers and _")
            return redirect(url_for("register"))
        
        if len(password) < 8 :
            flash("The password must be atleast 8 characters")
            return redirect(url_for("register"))
        
        secpassword = generate_password_hash(password)

        postcur.execute(
            "SELECT 1 FROM siteusers WHERE username = %s",
            (username,)
        )

        if postcur.fetchone():
            flash("Username already exists")
            postcur.close()
            conn.close()
            return redirect(url_for("register")) 

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
    
@app.route("/deleteaccount" , methods=["POST"])
def deleteaccount():
    if "username" not in session:
        return redirect(url_for("login"))
    
    conn = connection()
    cur3 = conn.cursor()

    cur3.execute(
        "DELETE FROM siteusers WHERE userid = %s",
        (session["userid"],)
    )

    conn.commit()
    cur3.close()
    conn.close()

    session.clear()

    flash("Account deleted successfully!")
    return redirect(url_for("login"))

