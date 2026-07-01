# Importing models
import datetime
import psycopg as postgres
from flask import Flask,request,session,render_template,redirect,url_for
from datetime import timedelta

# Settings
app = Flask(__name__)
app.secret_key = "Helloworld544313"
app.permanent_session_lifetime = datetime.timedelta(seconds=20)

# Getting connection
def get_connection():
    return postgres.connect(
        host = "localhost",
        dbname = "postgres",
        user = "postgres",
        password = "21200",
        port = 5432
    )

# Login Route
@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("loginform.html")

# The main route
@app.route("/")
def index():
    return redirect(url_for("login")) 

# The result route
@app.route("/result",methods=["POST"])
def show_the_final_result():
    username = request.form.get("username")
    password = request.form.get("password")
    user_id = request.form.get("userid")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO users(username,password,user_id)""",
        (username,user_id,password)
    )

    conn.commit()

    cur.close()
    conn.close()

    session["username"] = username
    session["userid"] = user_id

    session.permanent = True

    get_username = session.get("username")
    get_userid = session.get("userid")

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    return str(users)

# The logout route
@app.route("/logout",methods=["POST"])
def deleteing():
    session.clear()
    return "<h1>Informations deleted succesfully!</h1>"


