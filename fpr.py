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



@app.route("/api/users" , methods=["POST"])
def users():
    data = request.get_json()

    user = User(
        username = data["username"],
        user_email = data["user_email"]
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message" : "user created successfully!",
        "user" : {
            "id" : user.id,
            "username" : user.username,
            "user_email" : user.user_email
        }
    } , 201

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

@app.route("/api/useers")
def userss():
    data = User.query.all()

    result_list = []

    for username in data:
        result_list.append(
            {
                "id" : username.id,
                "username" : username.username
            }
        )

    return {
        "result" : result_list
    }

@app.route("/api/userss/<int:user_id>" , methods=["PUT"])
def user_with_update(user_id):
    user = User.query.get(user_id)

    if not user:
        return {
            "message" : "user not found bro!"
        } , 404

    mydata = request.get_json()

    user.username = mydata["username"]

    db.session.commit()

    return {
        "message" : "User updated successfully!",
        "user" : {
            "id" : user.id,
            "username" : user.username
        }
    }

@app.route("/api/userdelete/<int:user_id>" , methods=["DELETE"])
def delete_user_with_API(user_id):
    user = User.query.get(user_id)

    if not user:
        return {
            "message" : "Sorry! User not found!"
        } , 404

    db.session.delete(user)

    db.session.commit()

    return {
        "message" : "User deleted successfully!",
        "user" : {
            "id" : user.id,
            "username" : user.username
        }
    }


@app.route("/api/userssss" , methods=["POST"])
def json_test():
    data = request.get_json()

    if not data:
        return {
            "message" : "Ops! : Bad request"
        } , 400

    username = data.get("username" , "").strip()

    if not username:
        return {
            "message" : "Username already required!"
        } , 400

    useremail = data.get("user_email" , "").strip()

    if not useremail:
        return {
            "message" : "User email doesn't exists"
        } , 400

    return "op don!"

