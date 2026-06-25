from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "sinasina789"


@app.route("/", methods=["GET", "POST"])
def main_index():

    if request.method == "POST":

        username = request.form.get("username")
        user_id = request.form.get("id")

        session["username"] = username
        session["user_id"] = user_id

        print("SESSION AFTER SAVING:", dict(session))

        return redirect(url_for("show_situation"))

    return render_template("form.html")


@app.route("/situation")
def show_situation():

    print("SESSION IN SITUATION:", dict(session))

    username_s = session.get("username")
    id_s = session.get("user_id")

    if username_s is None or id_s is None:
        return "Please fill out the form!"

    return f"""
    <h1>Information</h1>
    <p>Username: {username_s}</p>
    <p>ID: {id_s}</p>
    """