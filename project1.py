from flask import Flask,request,render_template,make_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/welcome" , methods=["GET","POST"])
def say_welcome():
    username = None
    password = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return f"<h1>Your username is ({username})</h1> <h1>and your password is {password}</h1>"
    
    return render_template("result.html",username=username,password=password)

@app.route("/Set")
def setting():
    response = make_response("Cookie saved!")
    response.set_cookie("username","sina")
    return response

@app.route("/Get")
def getting():
    username = request.cookies.get("username")
    return f"Hello {username}"
