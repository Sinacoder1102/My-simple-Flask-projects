# Importing models
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from curses.ascii import isdigit
import re
from flask import Flask,request,redirect,render_template, session,url_for,flash
import psycopg
from datetime import timedelta
from werkzeug.security import generate_password_hash,check_password_hash

# Doing initial settings
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=2)
csrf = CSRFProtect(app)
limiter = Limiter(
    key_func=get_remote_address,
    app=app
)

# Connecting to postgres
def connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenve("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
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
        
        if not re.fullmatch(r"[A-Za-z0-9_]+" , username):
            flash("Username only contains letter,numbers and _")
            return redirect(url_for("register"))

        if username[0].isdigit():
            flash("The username can not start with numbers")
            return redirect(url_for("register"))
        
        if len(password) < 8 :
            flash("The password must be atleast 8 characters")
            return redirect(url_for("register"))

        if not re.search(r"[A-Z]" , password):
            flash("The password must contain atleast one uppercase letter")
            return redirect(url_for("register"))
        
        if not re.search(r"[a-z]" , password):
            flash("The password must contain atleast one lowercase letter")
            return redirect(url_for("register"))
        
        if not re.search(r"\d" , password):
            flash("The password must atleast contain one number")
            return redirect(url_for("register"))
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]" , password):
            flash("The password must contain atleast one special character")
            return redirect(url_for("register"))
        
        if not userid.isdigit():
            flash("The userid must be integer")
            return redirect(url_for("register"))
        
        if int(userid) <= 0:
            flash("The userid must be greater than 0!")
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
            "SELECT 1 FROM siteusers WHERE userid = %s",
            (userid,)        
            )
        
        if postcur.fetchone():
            flash("The userid is already exists")
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
@limiter.limit("5 per minute")
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
        flash("Wrong password!")
        return redirect(url_for("login"))
    
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
    
    new_username = request.form.get("username" , "").strip()

    if not new_username:
        flash("The new username is empty?")
        return redirect(url_for("editprof"))
    
    if len(new_username) < 3 :
        flash("The username must atleast contains 3 characters")
        return redirect(url_for("editprof"))

    if len(new_username) > 20 :
        flash("The username must not be more than 20 characters")
        return redirect(url_for("editprof"))

    if not re.fullmatch(r"[A-Za-z0-9_]+" , new_username):
        flash("The username must atleast contain letter,number and _")
        return redirect(url_for("editprof"))
    
    if new_username[0].isdigit():
        flash("The username can not start with numbers!")
        return redirect(url_for("editprof"))
    
    conn = connection()
    postcursor = conn.cursor()

    postcursor.execute(
    """
    SELECT 1
    FROM siteusers
    WHERE username = %s
    AND userid != %s
    """,
    (new_username, session["userid"])
    )

    if postcursor.fetchone():
        flash("Username already exists.")
        postcursor.close()
        conn.close()
        return redirect(url_for("editprof"))

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

@app.route("/updatepassword", methods=["POST"])
def updatepass():
    if "username" not in session:
        return redirect(url_for("login"))

    new_pass = request.form.get("newpassword", "").strip()
    old_pass = request.form.get("oldpassword", "").strip()

    with connection() as conn:
        with conn.cursor() as cur2:

            cur2.execute(
                "SELECT password FROM siteusers WHERE userid = %s",
                (session["userid"],)
            )

            user = cur2.fetchone()

            if user is None:
                flash("User not found!")
                return redirect(url_for("login"))

            db_password = user[0]

            if not old_pass or not new_pass:
                flash("One of the password fields is empty!")
                return redirect(url_for("changepassword"))

            if len(new_pass) < 8:
                flash("The password must contain at least 8 characters.")
                return redirect(url_for("changepassword"))

            if not re.search(r"[A-Z]", new_pass):
                flash("The password must contain at least one uppercase letter.")
                return redirect(url_for("changepassword"))

            if not re.search(r"[a-z]", new_pass):
                flash("The password must contain at least one lowercase letter.")
                return redirect(url_for("changepassword"))

            if not re.search(r"\d", new_pass):
                flash("The password must contain at least one number.")
                return redirect(url_for("changepassword"))

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_pass):
                flash("The password must contain at least one special character.")
                return redirect(url_for("changepassword"))

            if new_pass == old_pass:
                flash("The new password must be different from the current password.")
                return redirect(url_for("changepassword"))

            if check_password_hash(db_password, old_pass):
                new_hashed_password = generate_password_hash(new_pass)

                cur2.execute(
                    """
                    UPDATE siteusers
                    SET password = %s
                    WHERE userid = %s
                    """,
                    (new_hashed_password, session["userid"])
                )

                conn.commit()
                flash("Password updated successfully!")
                return redirect(url_for("showprof"))

            flash("Current password is incorrect!")
            return redirect(url_for("changepassword"))
    
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

