# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, length, Email, EqualTo
from FlaskBlog.models import User
from flask_login import current_user




class RegistrationForm(FlaskForm):
    
    username = StringField("Username", validators = [DataRequired(), 
                                                     length(min=2, max=20)])
    email = StringField("Email", 
                        validators = [DataRequired(), Email()])
    password = PasswordField("Password",
                             validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", 
                                     validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        
        if user!=None:
            raise ValidationError("Username is taken. Please choose a different username.")
            
    def validate_email(self,email):#CHECKS TO SEE IF USERNAME OR EMAIL ARE AVAILABLE
        user =  User.query.filter_by(email=email.data).first()
        
        if user!=None:
            raise ValidationError("Email is taken. Please choose a different email.")
            
    
    
class LoginForm(FlaskForm):
    
    email = StringField("Email", 
                        validators = [DataRequired(), Email()])
    password = PasswordField("Password",
                             validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    
    submit = SubmitField("Login")
    
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), 
                                                     length(min=2, max=20)])
    email = StringField("Email", 
                        validators = [DataRequired(), Email()])
    
    picture = FileField("Upload Profile Picture", 
                        validators = [FileAllowed(['jpg',"png","jpeg"])])
    
    submit = SubmitField("Update")
    
    def validate_username(self,username):
        if username.data!= current_user.username:
            user = User.query.filter_by(username=username.data).first()
            
            if user!=None:
                raise ValidationError("Username is taken. Please choose a different username.")
                
    def validate_email(self,email):#CHECKS TO SEE IF USERNAME OR EMAIL ARE AVAILABLE
        if email.data != current_user.email:
            user =  User.query.filter_by(email=email.data).first()
            
            if user!=None:
                raise ValidationError("Email is taken. Please choose a different email.")
                
                
class RequestResetForm(FlaskForm):
    email =  StringField("Email",
                         validators=[DataRequired(), Email()])
    
    submit = SubmitField("Request Password Reset")
    
    def validate_email(self,email):#CHECKS TO SEE IF USERNAME OR EMAIL ARE AVAILABLE
        user =  User.query.filter_by(email=email.data).first()
        
        if user==None:
            raise ValidationError("This email is not associated with any account yet. Please Register.")
    
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Passowrd", validators=[DataRequired()])
    
    confirm_password = PasswordField("Confirm Password", 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")
    
    
    