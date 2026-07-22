from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(100) , nullable = False)

    posts = db.relationship("Post" , backref = "user" , lazy = True)

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

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

    chosenuser = User.query.filter_by(username = username).first()

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

@app.route("/results")
def showeverything():
    user = User.query.all()
    for u in user:
        print(u.id , u.username)

    firstuser = User.query.first()
    if firstuser:
        print(firstuser.username)

    Aliuser = User.query.filter_by(username = "Ali").all()
    for al in Aliuser:
        print(al.username)

    userid = User.query.order_by(User.id).all()

    countuser = User.query.count()
    print(countuser)

    A_start = User.query.filter(User.username.startswith("A")).all()
    for use in A_start:
        print(use.username)

    return "Done Done!"

@app.route("/updateusername" , methods=["POST"])
def updateuser():
    old_username = request.form.get("oldusername")
    new_username = request.form.get("newusername")

    user = User.query.filter_by(username = old_username).first()

    if user:
        user.username = new_username
        db.session.commit()

    return "updating done"

@app.route("/deleteuser" , methods=["POST"])
def deletinguser():
    getuser = request.form.get("deleteduser" , "").strip()

    print("Input : " , getuser)
    
    deleted_user = User.query.filter_by(username = getuser).first()

    print("Found! : " , deleted_user)

    if deleted_user:
        db.session.delete(deleted_user)
        db.session.commit()
        return "User deleted successfully!"
    
    elif not getuser:
        return "The user is required!"
    
    else:
        return "<h1>Sorry! User not found!</h1>"
    
@app.route("/biggerthan2")
def ifbigger():
    biggerthan2 = User.query.filter(User.id > 2).all()

    for user in biggerthan2 :
        print(user.id , user.username)

    return "Done!"