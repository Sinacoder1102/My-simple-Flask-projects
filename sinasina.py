from flask import Flask,request,redirect,render_template,session,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,logout_user,UserMixin,current_user,login_required
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Secret-200"
app.permanent_session_lifetime = timedelta(seconds=20)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "mainregister"

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    user_email = db.Column(db.String(150) , nullable = False)

with app.app_context():
    db.create_all() 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return redirect(url_for("mainregister"))

@app.route("/mainform")
def mainregister():
    return render_template("registerform.html")

@app.route("/result" , methods=["POST"])
def show_result():
    user_information = request.form.get("email")

    if user_information:
        new_user = User(user_email = user_information) 

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        session.permanent = True

        return "<h1>User created and logged in successfully!</h1>"

    return "ops! : Adding user faild!"

@app.route("/profile")
@login_required
def show_profile():
    return f"<h1>User informations:</h1> <h2>User's id : {current_user.id}</h2> <h2>User's email : {current_user.user_email}</h2>"

@app.route("/dashboard")
@login_required
def dashboard_situation():
    return f"Welcome {current_user.user_email}"




        