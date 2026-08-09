from flask import Flask,render_template,redirect,request,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import selectinload 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maindata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(200) , nullable = False)
    role = db.Column(db.String(20) , default = "user")

    posts = db.relationship(
        "Post",
        back_populates = "user",
        cascade = "all, delete-orphan"
    )

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"))

    user = db.relationship(
        "User",
        back_populates = "posts",
        
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

        if found_user:
            return f"{found_user.username} -----> {found_user.id}"

        return "User said no!"
    
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


@app.route("/showall" , methods=["POST"])
def show_all_users():
    all_users = User.query.all()

    username_list= []

    user_id = []

    if all_users:
        for usernames in all_users:
            username_list.append(usernames.username)

        for userid in all_users:
            user_id.append(userid.id)

        return f"The users ----> {username_list} , ---------> The users' id ----> {user_id}"

    return "No user!"

@app.route("/addposts" , methods=["POST"])
def add_post():

    post_owner = request.form.get("username")
    post_title = request.form.get("post")

    if post_owner and post_title:

        try:
            user = User.query.filter_by(
                username=post_owner
            ).first()

            if user:

                new_post = Post(
                    title=post_title,
                    user=user
                )

                db.session.add(new_post)

                # raise Exception("Something went wrong!")

                db.session.commit()

                return "Post uploaded successfully!"

            return "User not found!"

        except Exception as e:

            db.session.rollback()

            return f"Error happened: {e}"

    return "Ops! problem in one of values!"

@app.route("/myposts" , methods=["POST"])
def show_user_posts():
    userinf = request.form.get("userposts")

    if userinf:
        user = User.query.options(
            selectinload(User.posts)
        ).filter_by(username = userinf).first()

        if user:
            results = []

            for post in user.posts:
                results.append(post.title)

            return f"{user.username} ------> {results}"

        return "User not found!"

    return "ops!"

@app.route("/fullinformation" , methods=["POST"])
def fullinfs():
    username = request.form.get("username")

    if username:
        user_selection = User.query.options(
            selectinload(User.posts)
        ).filter_by(username = username).first()

        if user_selection:
            posts = []

            for post in user_selection.posts:
                posts.append(post.title)

            return f"{user_selection.username} --------> {posts}"

        return "Ops! : User selectionloading faild!"

    return "Ops! : User not found!"

@app.route("/paginate" , methods=["POST"])
def show_paginate():

    pager = request.form.get("pagenumber" , type=int)

    user_paginate = User.query.paginate(
        page=pager,
        per_page=4
    )

    users = []

    for user in user_paginate.items:
        users.append(user.username)

    users_1 = []

    users_2 = []

    for usernames in user_paginate.next().items:
        users_1.append(usernames.username)

    for user_names in user_paginate.prev().items:
        users_2.append(user_names.username)

    

    return f"{users} <br> {users_1} <br> {users_2}"


@app.route("/test404")
def make_error():
    abort(404)
@app.errorhandler(404)
def handle_error(error):
    return render_template("404.html"),404

@app.route("/admin")
def admin():
    abort(403)
@app.errorhandler(403)
def answer_to_403(error):
    return "<h1>403</h1> <h2>This is 403 error!</h2>"

# دیباگر باید خاموش باشه تا نتیجه نمایش داده بشه
@app.route("/test500")
def make_500_error():
    x = 10 / 0
    return "Division done!"
@app.errorhandler(500)
def handle_500(error):
    return "Error! : division by 0 is impossible!" , 500





