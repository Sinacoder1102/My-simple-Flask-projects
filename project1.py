# Importing models
from flask import Flask,request,redirect,render_template, session,url_for
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
    
    return f"""Welcome {session["username"]}
    your id is {session["userid"]}
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
