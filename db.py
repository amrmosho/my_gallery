from flask_sqlalchemy import SQLAlchemy
import os

# from flask_session import Session
# from tempfile import mkdtemp

from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/images.db'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = './static/images/upload/'


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    banner = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<users %r>' % self.id


class images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    des = db.Column(db.String(255), unique=True, nullable=False)
    views = db.Column(db.String(255), unique=True, nullable=False)
    likes = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<images %r>' % self.title


def uploadimage(name):
    if request.method == 'POST':

        if name not in request.files:
            return False

        file1 = request.files[name]
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return path

    return False


def query(sql, o={}):
    result = db.engine.execute(sql, o)
    return result


def get_data(table_name, w=""):
    if w != "":
        w = " where " + w
    sql = f'select * from {table_name}  {w} '
    return query(sql)


def get_row(table_name, w="", c="*"):
    if w != "":
        w = " where " + w
    sql = f'select {c} from {table_name}  {w} '
    return query(sql).first()


def delete(table_name, w):
    sql = f'delete from {table_name}   WHERE {w}'
    return query(sql)


def insert(table_name, data):
    names = ""
    keys = ""
    sp = ""

    for key in data:
        keys += f'{sp} :{key}'
        names += f'{sp} {key}'
        sp = ","

    sql = f' INSERT INTO {table_name}({names}) VALUES ({keys})'
    return query(sql, data)


def update(table_name, data, w):
    sql_data = ""
    sp = ""

    for key in data:
        sql_data += f"{sp} `{key}`= :{key}"
        sp = ","

    sql = f' update  {table_name}  set  {sql_data} where {w}'
    return query(sql, data)


def get_images(user_id="", w=""):

    imgs = get_data("images", w)
    images = []
    for img in imgs:
        i = dict(zip(img.keys(), img))
        img_id = img["id"]
        img_user_id = img["user_id"]

        i["likes"] = get_row(
            "likes", f" `image_id`='{img_id}'", "count(id) as count ")["count"]

        is_uesr_like = get_row(
            "likes", f" `image_id`='{img_id}' and   `user_id`='{user_id}'")

        i["user_data"] = get_row("users", f" `id`='{img_user_id}'")

        if not is_uesr_like:
            i["user_like"] = "0"
        else:
            i["user_like"] = "1"
        images.append(i)

    return images
