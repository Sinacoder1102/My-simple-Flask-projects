# Importing models
from flask import Flask,request,redirect,render_template,session,url_for
from datetime import timedelta
import psycopg
from werkzeug.security import generate_password_hash,check_password_hash

# Giving the initial settings
app = Flask(__name__)
app.secret_key = "Sina-secret-key243"
app.permanent_session_lifetime = timedelta(minutes=5)

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

    hashed_pass = generate_password_hash(password)

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
        password VARCHAR(500) NOT NULL,
        age INTEGER 
        )"""
    )

    # Checking the username
    postgres_cursor.execute(
        "SELECT username FROM siteusers WHERE username = %s",
        (username,)
    )

    exiting_user = postgres_cursor.fetchone()

    if exiting_user:
        postgres_cursor.close()
        conn.close()

        return "This username is already exists."

    # Adding users to database
    postgres_cursor.execute(
        """INSERT INTO siteusers(username,password,age) VALUES (%s,%s,%s)""",
        (username,hashed_pass,age)
    )
    conn.commit()

    # Closing 
    postgres_cursor.close()
    conn.close()

    return f"Informations saved successfully! {render_template("deletelog.html")}"

@app.route("/logout",methods=["POST"])
def logout_user():
    session.clear()
    return "You logged out successfully!"


@app.route("/delete_account",methods=["POST"])
def delete_user():
    if "username" not in session:
        return redirect(url_for("loginuser"))
    
    username = session["username"]

    conn = connection()
    cur = conn.cursor()

    print("Deleting:", username)

    cur.execute(
        "DELETE FROM siteusers WHERE username = %s",
        (username,)
    )

    conn.commit()

    cur.close()
    conn.close()


    session.clear()

    return "<h2>The informations deleted successfully!</h2>"



@app.route("/login_check",methods=["POST"])
def checkiflogin():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = connection()
    postgres_cur = conn.cursor()

    postgres_cur.execute(
        "SELECT password,age FROM siteusers WHERE username = %s",
        (username,)
    )

    user = postgres_cur.fetchone()

    if user is None:
        return "<h3>The Username doesn't exist.</h3>"

    if check_password_hash(user[0] , password):
        session.permanent = True
        session["username"] = username
        session["age"] = user[1]

        postgres_cur.close()
        conn.close()

        return redirect(url_for("dashboard"))
    
    postgres_cur.close()
    conn.close()

    return "<h1>The Wrong password........</h1>"
    

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("loginuser"))

    return f"""<h1>Welcome {session["username"]}</h1> <h2>Your age is {session["age"]}</h2>""" 
   
@app.route("/register")
def register():
    return render_template("register.html")