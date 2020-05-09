# -*- coding: utf-8 -*-
from FlaskBlog import db
from FlaskBlog.models import Post
from FlaskBlog.posts.forms import PostForm

from flask import render_template, url_for, redirect,flash, abort, request, Blueprint
from flask_login import current_user, login_required


posts = Blueprint("posts",__name__)

@posts.route("/post/new", methods=["GET","POST"])
@login_required
def new_post():
    
    form = PostForm()
    
    if  form.validate_on_submit(): 
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)#add post from database
        db.session.commit()
        flash("Your Post Has Been Created","success")
        return redirect(url_for("main.home"))
    
    return render_template("create_post.html",title="New Post", 
                           legend="New Post",form=form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #returns a 404 message is the post does not exist 
    return render_template("post.html", title=post.title, post=post)

#route to update/delete posts
@posts.route("/post/<int:post_id>/update", methods=["GET","POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    
    if post.author != current_user:#check to make sure only author can update post
        abort(403)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data #actually update the post in database
        db.session.commit()
        flash("Your Post Has Been Updated", "success")
        return redirect(url_for("posts.post",post_id=post.id))
    
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template("create_post.html", title="Update Post", 
                           legend="Update Post",form=form)



@posts.route("/post/<int:post_id>/delete", methods=["GET","POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash("Your Post Has Been Deleted", "success")
    return redirect(url_for("main.home"))
        


