import os
import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from db import *
# from flask_session import Session
# from tempfile import mkdtemp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = './static/images/upload/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'


def get_login_data():
    if 'user_login_data' in session:
        return get_row(
            "users", "id='" + str(session['user_login_data']) + "'")
    else:
        return ""


@ app.route('/<page>', methods=['GET', 'POST'])
def user_home(page="1"):
    if 'user_login_data' in session:
        login_user_data = get_login_data()
        user_id = str(login_user_data["id"])
        follow = get_data("follow", f"user_id='{user_id}'")
        follow_user_data = []
        for f in follow:
            follow_user_data.append(
                get_row("users", "id='" + str(f['follower']) + "'"))

        limit = 9
        images_count = get_row("images", "", "count(id) as cid")["cid"]
        get_from = limit * (int(page) - 1)
        images = get_images(user_id, f"1=1 limit {get_from},{limit}")

        page = int(page)
        next = page + 1
        perv = page - 1
        count = int(int(images_count)/limit)+1
        pages = {"next": next, "page": page,
                 "perv": perv, "count": count}

        return render_template("users_home.html", menu="home", pages=pages, images=images, login_user_data=login_user_data, follow_user_data=follow_user_data)
    else:
        return redirect("/", code=302)


@ app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_login_data' in session:
        return user_home()
    else:
        if request.method == 'POST':
            sql = "select * from users where email= :email and password= :password "
            o = {'password': request.form.get(
                "password"), 'email': request.form.get("email")}
            user_data = db.engine.execute(sql, o).first()

            if not user_data:
                return render_template("home.html", menu="home", errormsg="login error :(")
            else:
                session['user_login_data'] = user_data[0]
                return redirect("/mypage", code=302)

        return render_template("home.html", menu="home")


# pages
@app.route('/user/<id>/<page>', methods=['GET', 'POST'])
@app.route('/user/<id>', methods=['GET', 'POST'])
def user(id, page="1"):
    if 'user_login_data' in session:
        user_data = get_row("users", f"id='{id}'")
        login_user_data = get_login_data()
        user_id = str(login_user_data["id"])
        follow = is_follow(user_id,  id)
        w = f"user_id ={id}"
        limit = 9
        images_count = get_row("images", w, "count(id) as cid")["cid"]
        get_from = limit * (int(page) - 1)
        images = get_images(user_id, f" {w} limit {get_from},{limit}")

        page = int(page)
        next = page + 1
        perv = page - 1
        count = int(int(images_count)/limit)+1
        pages = {"next": next, "page": page,
                 "perv": perv, "count": count}

        return render_template("user.html", follow=follow,  menu="user", pages=pages, images=images, user=user_data, login_user_data=login_user_data)
    else:
        return redirect("/", code=302)


@app.route('/search/<word>/', methods=['GET', 'POST'])
@app.route('/search/<word>/<page>', methods=['GET', 'POST'])
def search(word, page="1"):
    if 'user_login_data' in session:
        login_user_data = get_login_data()
        user_id = str(login_user_data["id"])

        limit = 9
        w = f"( title like '%{word}%'  or des like'%{word}%' )  "
        images_count = get_row("images", w, "count(id) as cid")["cid"]
        get_from = limit * (int(page) - 1)
        images = get_images(user_id, f" {w } limit {get_from},{limit}")

        page = int(page)
        next = page + 1
        perv = page - 1
        count = int(int(images_count)/limit)+1
        pages = {"next": next, "page": page,  "images_count": images_count,
                 "perv": perv, "count": count}

        return render_template("search.html", menu="search", search=word,  pages=pages, images=images, login_user_data=login_user_data)
    else:
        return redirect("/", code=302)


@app.route('/explore/', methods=['GET', 'POST'])
@app.route('/explore/<page>', methods=['GET', 'POST'])
def explore(page="1"):
    if 'user_login_data' in session:
        login_user_data = get_login_data()
        user_id = str(login_user_data["id"])

        limit = 9
        images_count = get_row("images", "", "count(id) as cid")["cid"]
        get_from = limit * (int(page) - 1)
        images = get_images(user_id, f"1=1 limit {get_from},{limit}")

        page = int(page)
        next = page + 1
        perv = page - 1
        count = int(int(images_count)/limit)+1
        pages = {"next": next, "page": page,
                 "perv": perv, "count": count}

        return render_template("explore.html", menu="explore", pages=pages, images=images, login_user_data=login_user_data)
    else:
        return redirect("/", code=302)


@app.route('/mypage/<page>', methods=['GET', 'POST'])
@ app.route('/mypage', methods=['GET', 'POST'])
def mypage(page="1"):
    if 'user_login_data' in session:
        saveimage()

        login_user_data = get_login_data()
        user_id = str(login_user_data["id"])
        w = f"user_id ={user_id}"
        limit = 9
        images_count = get_row("images", w, "count(id) as cid")["cid"]
        get_from = limit * (int(page) - 1)
        images = get_images(user_id, f" {w} limit {get_from},{limit}")

        page = int(page)
        next = page + 1
        perv = page - 1
        count = int(int(images_count)/limit)+1
        pages = {"next": next, "page": page,
                 "perv": perv, "count": count}

        return render_template("mypage.html", menu="mypage",  pages=pages,   images=images, login_user_data=login_user_data)
    else:
        return redirect("/", code=302)


@ app.route('/about', methods=['GET', 'POST'])
def about(page="1"):
    login_user_data = get_login_data()
    return render_template("about.html", menu="about", login_user_data=login_user_data)

# pages


# user Actions

@ app.route('/logout')
def logout():
    session.pop('user_login_data', None)
    return redirect("/mypage", code=302)


@ app.route('/edit_my_data/', methods=['GET', 'POST'])
def edit_my_data():
    if request.method == 'POST':
        sql = ' update  users  set `name`="' + request.form.get("name") + '"'
        sql += ' ,  `email`="' + request.form.get("email") + '" '
        sql += ' ,  `password`="' + request.form.get("password") + '" '

        if ("image" in request.form):
            sql += ' ,  `image`="' + request.form.get("image") + '" '

        if ("banner" in request.form):
            sql += ' ,  `banner`="' + request.form.get("banner") + '" '

        sql += 'WHERE id = :val'
        result = db.engine.execute(sql, {'val': request.form.get("user_id")})
        return redirect("/mypage", code=302)

    else:
        if 'user_login_data' in session:
            user_data = users.query.filter_by(
                id=session['user_login_data']).first_or_404()
        return render_template("profile.html",  user=user_data)


@ app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        image = uploadimage("image")
        banner = uploadimage("banner")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = f' INSERT INTO users(name,email,password,image,banner) VALUES ("{name}", "{email}","{password}", "{image}" ,"{banner}")'
        result = db.engine.execute(sql)
        return redirect("/", code=302)
    else:
        return render_template("signup.html")

        # images Actions


@ app.route('/follow/<follow_id>/<user_id>')
def follow_unfollow(follow_id, user_id):
    w = f"`follower`='{follow_id}' and  `user_id`='{user_id}'"
    old_data = get_row("follow", w)

    if not old_data:
        old_data = insert(
            "follow", {"follower": follow_id, "user_id": user_id, })
        return f"<div onclick='follow_user(this)' data-follow_id='{follow_id}' data-user_id='{user_id}'  class='red_bg  col-4'> <i  class = 'fas fa-user-check' > </i > Following</div>"
    else:
        old_data = delete("follow", w)
        return f"<div onclick='follow_user(this)' data-follow_id='{follow_id}' data-user_id='{user_id}'  class='blue_bg  col-4'> <i  class = 'fas fa-user' > </i > Follow</div>"


def is_follow(user_id, follower_id):
    w = f"user_id='{user_id}' and  follower='{follower_id}'"
    follow_data = get_row("follow", w)
    if not follow_data:
        return "0"
    else:
        return "1"
# user Actions


# images Actions

def saveimage():
    if request.method == 'POST':
        if not request.form.get("title"):
            return "must provide title"

        if 'src' not in request.files:
            return 'there is no src in form!'
        file1 = request.files['src']

        if request.form.get("status") == "add":
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(path)
            a = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            insert("images", {"src": path, "title": request.form.get("title"), "des": request.form.get(
                "des"), "views": "0", "likes": "0", "created": a, "user_id": request.form.get("user_id")})

        else:

            sql = ' update  images  set `title`="' + \
                request.form.get("title") + '"'

            sql += ' ,  `des`="' + request.form.get("des") + '" '

            if file1.filename != "":
                path = os.path.join(
                    app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(path)
                sql += ' ,  `src`="' + path + '" '

            sql += 'WHERE id = :val'
            result = db.engine.execute(
                sql, {'val': request.form.get("image_id")})


@ app.route('/image/<id>')
def image(id):
    login_user_data = get_login_data()
    user_id = str(login_user_data["id"])

    img = get_images(user_id, f"id='{id}'")[0]

    follow = is_follow(user_id,  str(img["user_data"][0]))

    old_views = int(img["views"])
    views = old_views + 1
    img["views"] = views
    update("images", {"views": views}, f"id='{id}'")
    return render_template("image.html",  img=img, follow=follow, login_user=login_user_data)


@ app.route('/addimage')
def addimage():
    user_data = users.query.filter_by(id='1').first_or_404()
    return render_template("add_image.html",  user=user_data)


@ app.route('/editimage/<id>')
def editimage(id):
    user_data = users.query.filter_by(id='1').first_or_404()
    image = images.query.filter_by(id=id).first_or_404()
    return render_template("add_image.html",  user=user_data, image=image)


@ app.route('/deleteimage/<id>')
def delete_image(id):
    if not id:
        return "must provide id"
    sql = ' delete from images   WHERE id = :val'
    result = db.engine.execute(sql, {'val': id})
    return "Image was successfully deleted"


@ app.route('/imagelike/<image_id>/<user_id>')
def add_remove_like(image_id, user_id):
    w = f"`image_id`='{image_id}' and  `user_id`='{user_id}'"
    old_data = get_row("likes", w)

    color_class = ""

    if not old_data:
        old_data = insert(
            "likes", {"image_id": image_id, "user_id": user_id, })
        color_class = "red_color"
    else:
        old_data = delete("likes", w)

    likes = get_row(
        "likes", f" `image_id`='{image_id}'", "count(id) as count ")["count"]

    return f' <span onclick = "like_image(this)" data-image_id = "{image_id}" data-user_id = "{user_id}" class = "col-3 img_like_btn     small-info " > <i style = "width:auto ;margin: 0 5px;" class = "far  {color_class}   fa-thumbs-up" > </i > {likes} </span >'

# images Actions
