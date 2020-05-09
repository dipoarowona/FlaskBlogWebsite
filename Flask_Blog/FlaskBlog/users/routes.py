# -*- coding: utf-8 -*-
from FlaskBlog import db, bcrypt
from FlaskBlog.users.forms import (RegistrationForm, LoginForm,
                             UpdateAccountForm, ResetPasswordForm, RequestResetForm)
from FlaskBlog.models import User, Post
from FlaskBlog.users.utils import save_pic, send_reset_email

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user,login_required, logout_user



users = Blueprint("users",__name__)

@users.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if form.validate_on_submit():
        
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit() #passoword from user is hashed then information is added to database
        
        #check to see  if email or username is in  database
        
        flash(f"Account Has Been Created. You Can Now Login!", "success")#sends success message to the user when submit form
        return redirect(url_for("users.login"))
    return render_template("register.html", title = "Register", form = form)

@users.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:#if user is already logged in when they click on the login or register it redirects them to the home page
        return redirect(url_for("main.home"))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user!=None and bcrypt.check_password_hash(user.password,form.password.data) :
            #checks to see if there email is valid and login them in
            login_user(user,remember=form.remember.data)
            nextpage = request.args.get('next')
            return redirect(nextpage) if nextpage!=None else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful, Please Try Again", "danger")
    return render_template("login.html", title = "Login", form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            current_user.profile_image = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()#send to databse
        flash("Your Account Has Been Updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":#this is so that the text fields already have the user info displayed
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    imgfile = url_for("static", filename = "profile_pics/"+current_user.profile_image)
    return render_template("account.html",title="Account", image_file=imgfile, form=form)

@users.route("/user/<string:username>")#route for all posts for each user
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.time.desc()).paginate(page=page, per_page=5)
        #gets all post by certain author
        #then sorts them in descending order
        #paginates them to 5 a page
    return render_template("user_post.html", posts=posts, user=user)

@users.route("/reset_password", methods=["GET","POST"])#route for all posts for each user
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home")) #send the user the home page if they are already logged in 
   
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("email has been sent to "+user.email+" with further instructions.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)



@users.route("/reset_password/<token>", methods=["GET","POST"])#route for all posts for each user
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home")) #send the user the home page if they are already logged in 
    
    user = User.verify_reset_token(token)
    
    if user is None:
        flash("This is invalid or an expired token!", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pw
        db.session.commit() #passoword from user is hashed then information is updated to database
        
        flash("Your Password Has Been Updated!", "success")#sends success message to the user when submit form
        return redirect(url_for("users.login"))
    
    return render_template("reset_token.html", title="Reset Password", form=form)

