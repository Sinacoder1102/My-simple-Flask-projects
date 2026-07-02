# Importing models
from flask import Flask,request,redirect,render_template, session,url_for
from datetime import timedelta
import psycopg

# Giving the initial settings
app = Flask(__name__)
app.secret_key = "Sina-secret-key243"
app.permanent_session_lifetime = timedelta(seconds=20)

# Getting connection from postgres
def connection():
    return psycopg.connect(
        host = "localhost",
        dbname = "postgres",
        user = "postgres",
        password = "21200",
        port = 5432
    )

# The login route
@app.route("/login")
def loginuser():
    return render_template("loginform01.html")

# Just a route for redirecting to the login tab
@app.route("/",methods=["GET","POST"])
def return_to_loginform():
    return redirect(url_for("loginuser"))

# Saving informatios 
@app.route("/savinginfs",methods=["POST"])
def show_ways():
    # Making initial variables
    username = request.form.get("username")
    password = request.form.get("password")
    age = request.form.get("age")

    # Defining variables of postgres
    conn = connection()
    postgres_cursor = conn.cursor()

    # Activing the session's time
    session.permanent = True

    # Defining sessions
    session["username"] = username
    session["age"] = age

    # Making a table
    postgres_cursor.execute(
        """CREATE TABLE IF NOT EXISTS siteusers(
        id SERIAL PRIMARY KEY,
        username VARCHAR(60) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        age INTEGER 
        )"""
    )

    # Adding users to database
    postgres_cursor.execute(
        """INSERT INTO siteusers(username,password,age) VALUES (%s,%s,%s)""",
        (username,password,age)
    )
    conn.commit()

    # Closing 
    postgres_cursor.close()
    conn.close()

    return "Informations saved successfully!"