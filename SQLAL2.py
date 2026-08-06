from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maindata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(200) , nullable = False)

    posts = db.relationship(
        "Post",
        back_populates = "user"
    )

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"))

    user = db.relationship(
        "User",
        back_populates = "posts"
    )

with app.app_context():
    db.create_all()

@app.route("/")
def mainindex():
    return redirect(url_for("mainpage"))

@app.route("/mainform")
def mainpage():
    return render_template("SQLA.html")

@app.route("/added" , methods=["POST"])
def add_user():
    user = request.form.get("username")

    if user:
        username1 = User(username = user)

        db.session.add(username1)
        db.session.commit()

        return "Adding user done!"

@app.route("/find" , methods=["POST"])
def find_user():
    find1 = request.form.get("username")

    if find1:
        found_user = User.query.filter_by(username = find1).first()

        return f"{found_user.username} -----> {found_user.id}"

    return "User not found!"

@app.route("/updateusername" , methods=["POST"])
def update_user():
    old_user = request.form.get("oldusername")
    new_user = request.form.get("newusername")

    if old_user and new_user:
        update_user1 = User.query.filter_by(username = old_user).first()

        if update_user1:
            update_user1.username = new_user
            db.session.commit()
            return "User updated successfully!"

        return "User not found!"

    return "Please enter both variables!"

@app.route("/deleteuser" , methods=["POST"])
def deleteing():
    dead_user = request.form.get("deleteduser")

    if dead_user:
        user_del = User.query.filter_by(username = dead_user).first()

        if user_del:
            db.session.delete(user_del)
            db.session.commit()

            return "User deleted successfully!"

        return "User not found!"

    return "I really don't know what should I say"



