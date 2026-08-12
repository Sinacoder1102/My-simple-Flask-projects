from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

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
    return redirect(url_for("loginform"))

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


ALLOWED_EXTENSIONS = {"png" , "jpg" , "jpeg"}

@app.route("/upload" , methods=["POST"])
def upload_file():
    file_get = request.files.get("uploadfile")

    def allowed_file(filename):
        return "." in filename and \
                filename.rsplit("." , 1)[1].lower() in ALLOWED_EXTENSIONS

    if not file_get:
        return "No file!"

    if not allowed_file(file_get.filename):
        return "file type not allowed!"

    filename = secure_filename(file_get.filename)
    print(filename)

    file_get.save("uploads/" + filename)

    return "File uploaded successfully!"

@app.errorhandler(RequestEntityTooLarge)
def hanle_this_file(error):
    return "<h1>Ops! : File length is very larger than 1 mb</h1>" , 413



@app.route("/api/users")
def users():
    username = User.query.all()

    return {
        "users" : [
            {
                "id" : user.id,
                "username" : user.username
            }
            for user in username
        ]
    }

@app.route("/api/users/<int:user_id>")
def users_in_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return "Ops! : User not found!" , 404

    return {
        "id" : user.id,
        "username" : user.username,
        "email" : user.user_email
    }
