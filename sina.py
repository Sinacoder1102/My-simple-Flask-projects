from flask import Flask,request,render_template


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello to the world of programing!"


@app.route("/practice", methods=["GET", "POST"])
def practice():
    print("METHOD:", request.method)
    print("ARGS:", request.args)
    print("FORM:", request.form)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return f"{username} - {password}"

    return render_template("form.html")




