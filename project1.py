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

# Creating the table
connect = connection()
cur1 = connect.cursor()

cur1.execute(
    """CREATE TABLE IF NOT EXISTS siteusers(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL,
    userid INTEGER NOT NULL

    )"""
)
connect.commit()
cur1.close()
connect.close()

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
        session["password"] = password
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

        return "<h3>Account created successfully!</h3>"
    
    except Exception as ex:
        return f"Ops!!!!!!! : {ex}"
    


