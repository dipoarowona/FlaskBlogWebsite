# -*- coding: utf-8 -*-
import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import url_for, current_app

from FlaskBlog import  mail

def save_pic(form_picture):
    random_hex = secrets.token_hex(8) #create random hex for the picture
    _, pic_type = os.path.splitext(form_picture.filename)#get pic name and file extension/type(png or jpg)
    picture_fn = random_hex + pic_type #picture filename
    
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)
    #creates the path on our computer where  we  want to save the picture
    output_size = (125,125)
    i = Image.open(form_picture)#image is resized to the default 125x125
    i.thumbnail(output_size)
    
    i.save(picture_path) #picture is saved
    
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", 
                  sender="noreplyarowona@gmail.com", 
                  recipients=[user.email])
    
    
    msg.body = f'''To reset your password, visit the following link: 
{ url_for('users.reset_token', token=token, _external=True) }
    
If you did not make this request, then simply ignore the previous and no changes will be made
    '''
    mail.send(msg)
