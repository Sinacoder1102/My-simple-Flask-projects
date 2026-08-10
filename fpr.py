from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "loginform"
app.secret_key = "This-is-a-secret-key"

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(200) , nullable = False)
    user_email = db.Column(db.String(500))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/mainlogin")
def loginform():
    return render_template("fpr.html")

@app.route("/users" , methods=["POST"])
def show_user_situation():
    user1 = request.form.get("username" , "").strip()

    if user1:
        user = User(username = user1)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return "User created and logged in successfully!"

    return "User not found!"

@app.route("/logincheck")
@login_required
def login_check_required():
    username = current_user.username
    userid = current_user.id

    print(current_user)
    print(current_user.username)
    print(current_user.id)

    return render_template("profile.html" , username = username , userid = userid)

@app.route("/logoutuser" , methods=["POST"])
@login_required
def log_out():
    username = current_user.username

    logout_user()

    return "User logged out successfully!"


