# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template
from FlaskBlog.models import Post

main = Blueprint("main", __name__)

@main.route("/")#routes are different pages on the website 
@main.route("/home")
def home():
    page = request.args.get("page",1,type=int)#get the page we  want in the url
    post = Post.query.order_by(Post.time.desc()).paginate(page=page, per_page=5)#get posts from database per page in descending order
    return render_template("home.html", posts = post)

@main.route("/about")
def about():
    return render_template("about.html", title = "About")

