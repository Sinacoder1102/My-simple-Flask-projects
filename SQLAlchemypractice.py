from flask import Flask,redirect,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_,func,exists
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model): 
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(100) , nullable = False)

    posts = db.relationship("Post" , back_populates = "user")

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(500))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    user = db.relationship(
        "User",
        back_populates = "posts"
    )

class Employee(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    manager_id = db.Column(db.Integer , db.ForeignKey("employee.id"))


with app.app_context():
    db.create_all()



@app.route("/")
def redirecting():
    return redirect(url_for("addingform"))

@app.route("/form")
def addingform():
    return render_template("SQLA.html")

@app.route("/added" , methods=["POST"])
def addeduser():
    username = request.form.get("username" , "").strip()

    if username:
        user = User(username = username)

        db.session.add(user)
        db.session.commit()
        return "Adding user Done!"

@app.route("/find" , methods=["POST"])
def find():
    founduser = request.form.get("username" , "").strip()

    querying = User.query.filter_by(username = founduser).first()

    if querying:
        for i in querying:
            return f"The users with this infs : {i.id , i.username}"

@app.route("/updateusername", methods=["POST"])
def updateuser():
    old_user = request.form.get("oldusername", "").strip()
    new_user = request.form.get("newusername", "").strip()

    if old_user and new_user:
        user = User.query.filter_by(username=old_user).first()

        if user:
            user.username = new_user
            db.session.commit()
            return "User updated successfully!"

        return "User not found!"

    return "Please enter both usernames!"

@app.route("/deleteuser", methods=["POST"])
def delete_user():
    username = request.form.get("deleteuser", "").strip()

    if username:
        user = User.query.filter_by(username=username).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully!"

        return "User not found!"

    return "Please enter a username!"

@app.route("/users" , methods=["GET"])
def showusers():
    allusers = User.query.all()

    usernames = []

    for user in allusers:
        usernames.append(user.username)

    return f"<h2>You can see users in this tab -------> {usernames}</h2>"
    
@app.route("/addposts" , methods=["POST"])
def add_user_post():
    username = request.form.get("username")
    post = request.form.get("post")

    if username:
        user = User.query.filter_by(username = username).first()
        new_post = Post(user = user , title = post)

        db.session.add(new_post)
        db.session.commit()
        return "Post created successfully!"
    

@app.route("/myposts" , methods=["POST"])
def see_posts():
    user_informations = request.form.get("userposts")

    user = User.query.filter_by(username = user_informations).first()

    if user:
        for post in user.posts:
            print(post.title)
        return "See posts from the terminal!"


@app.route("/orderedusers")
def ordering():
    users = User.query.order_by(User.username).all()

    result = []

    for user in users:
        result.append(user.username)

    return "<br>".join(result)

@app.route("/showrecords")
def showrecords():
    user = User.query.order_by(User.username).offset(1).limit(9).all()

    if user:
        result = []

        for i in user:
            result.append(i.username)

        return "<br>".join(result)

@app.route("/agfuncs")
def show_agfuncs():
    user_count = User.query.count()

    print(user_count)

    return "EDone"

@app.route("/andor")
def test():
    or_user = User.query.filter(
        or_(
            User.username == "Ali",
            User.id > 3
        )
    ).all()

    and_user = User.query.filter(
        and_(
            User.username != "Akbar",
            User.id > 5
        )
    ).all()


    or_user_list = []

    and_user_list = []


    if or_user:
        for p in or_user:
            or_user_list.append(p.username)

        # return f"{or_user_list}"

    if and_user:
        for l in and_user:
            and_user_list.append(l.username)

        return f"{and_user_list} <br> {or_user_list}"


@app.route("/intest")
def intest():
    user = User.query.filter(
        User.username.in_(["mammad4" , "Zohreh454" , "Saba230"])
    ).all()

    users = []

    if user:
        for i in user:
            users.append(i.id)
        return f"Hello man ------>  {users}"

@app.route("/join")
def join():
    posts = db.session.query(Post).join(User).filter(User.username == "Ali").all()

    aliposts = []

    if posts:
        for u in posts:
            print(u.title)
        return "Howwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"


@app.route("/statistics")
def statics():
    count_user = db.session.query(
        func.count(User.id)
    ).scalar()

    max_user = db.session.query(
        func.max(User.id)
    ).scalar()

    min_user = db.session.query(
        func.min(User.id)
    ).scalar()

    avg_user = db.session.query(
        func.avg(User.id)
    ).scalar()

    sum_user = db.session.query(
        func.sum(User.id)
    ).scalar()

    return f"<h3>counting users = {count_user} , max user's id = {max_user} , minimum user's id = {min_user} , average = {avg_user} , sum of users = {sum_user} !</h3>"


@app.route("/groupby")
def grouping():
    users = db.session.query(
        User.username,
        func.count(Post.id),
    ).join(Post).group_by(User.id).all()

    outing = []

    if users:
        for username,count in users:
            outing.append(f"{username} -> {count} posts")
        return "<br>".join(outing)

@app.route("/having")
def haveit():
    having = db.session.query(
        User.username,
        func.count(Post.id),
    ).join(Post).group_by(User.id).having(func.count(Post.id) > 1).all()

@app.route("/subquery")
def subquery():
    subquery1 = db.session.query(
        Post.user_id
    )

    users = User.query.filter(
        User.id.in_(subquery1)
    ).all()

    

@app.route("/manager")
def manager():

    Manager = aliased(Employee)

    employees = db.session.query(
        Employee.name,
        Manager.name
    ).join(Manager , Employee.manager_id == Manager.id).all()

    result = []

    for username , user_manager in employees:
        return f"{username} ---->  {user_manager}"

    return "<br>".join(result)

@app.route("/outerjoin")
def outerjoin():
    users = db.session.query(
        User.username,
        Post.title
    ).outerjoin(Post).all()

    for username , post in users:
        print(username , post)

    return "Done bro"

# @app.route("/thisismyend")
# def disid():
#     user = db.session.query(
#         exists().where(User.username == "ALi")
#     ).scalar()

@app.route("/union")
def unioning():
    query1 = db.session.query(
        User.username
    ).filter(User.username.contains("Ali"))

    query2 = db.session.query(
        User.username
    ).filter(User.id < 3)

    result = query1.union(query2).all()

    for i in result:
        print(i.username)

    return "Done successfully!"

