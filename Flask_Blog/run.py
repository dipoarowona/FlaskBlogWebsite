#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:14:40 2020

@author: dipoarowona
"""
#ENVIRONMENT VARIABLE 
# = export FLASK_APP=FlaskBlog.py
#RUN FLASK FROM COMMAND LINE
#flask run

#when runninng in browser we can use 'localhost' instead of our ip address

#we can run in debug mode via terminal or in the flask source code
#terminal - export FLASK_DEBUG=1
#source code - below
from FlaskBlog import create_app

app = create_app()
#debug mode
if __name__ == "__main__":
    app.run(debug=True)

#only purpose of this file is to run















    
    