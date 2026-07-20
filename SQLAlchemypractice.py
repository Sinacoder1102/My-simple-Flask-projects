from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(100) , nullable = False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("addusers"))

@app.route("/addyourself")
def addusers():
    return render_template("SQLA.html")


@app.route("/added" , methods=["POST"])
def added_user():

    username = request.form.get("username" , "").strip()

    if not username:
        return "The username required!"
    
    user = User(username = username)

    db.session.add(user)
    db.session.commit()

    return "Opration done successfully!"
 

@app.route("/find" , methods=["POST"])
def findusers():
    username = request.form.get("username" , "").strip()

    chosenuser = User.query.filter_by(username = username).all()

    if chosenuser:
        return f"<h1>{chosenuser.username}</h1>"
    else:
        return "User not found!"

@app.route("/users")
def show_users():
    users = User.query.all()

    for user in users:
        print(user.id , user.username)

    return "Done!"
