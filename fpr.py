from os import abort

from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,current_user,login_required,logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "sinasecret123"

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(100) , nullable = False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def redirecting():
    return redirect(url_for("loginform"))

@app.route("/login")
def loginform():
    return render_template("fpr.html")

@app.route("/users" , methods=["POST"])
def create_user():
    user = request.form.get("username" , "").strip()

    if user:
        created_user = User(username = user)

        db.session.add(created_user)
        db.session.commit()

        login_user(created_user)

        return "User created and logged in successfully!"

    return "User not found!"

@app.route("/profile")
@login_required
def profile():

    username = current_user.username
    userid = current_user.id

    print(current_user)
    print(current_user.username)
    print(current_user.id)

    return render_template("logout.html" , username=username,userid=userid)

@app.route("/logout" , methods=["POST"])
@login_required
def logout_user_s():
    username = current_user.username

    logout_user()

    return "The user logged out successfully!"



