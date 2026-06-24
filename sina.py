from flask import Flask,request,render_template

app = Flask(__name__)

@app.route("/",methods=["GET" , "POST"])
def start():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return f"Username is {username}"
    
    return render_template("form.html")

@app.route("/result-route" , methods=["POST" , "GET"])
def show():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("result.html",username=username,password=password)
    

