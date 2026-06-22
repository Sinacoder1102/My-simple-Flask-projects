from flask import Flask,request,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello to the world of programing!"


@app.route("/practice")
def index1():
    username = request.args.get("username")
    password = request.args.get("password")
    return render_template("form.html",username=username,password=password)


