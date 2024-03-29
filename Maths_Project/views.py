from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import db
import json
from models import User
import random


views = Blueprint('views', __name__)

from database_attempt import *


@views.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == "POST":
        button1 = request.getParameter("button1");
        print(button1)
    return render_template("main_page.html", user=current_user)

@views.route('/TEACHERhome', methods=['GET', 'POST'])
@login_required
def teacher_home():
    with open("quotes.txt") as quotes:  
        all_quote = quotes.readlines()
        quote = random.choice(all_quote)

    return render_template("teacher_home.html", user = current_user, name = current_user.first_name, quote = quote)




@views.route('/STUDENThome', methods=['GET', 'POST'])
@login_required
def student_home():
    with open("quotes.txt") as quotes:  
        all_quote = quotes.readlines()
        quote = random.choice(all_quote)


    return render_template("home.html", user=current_user, name = current_user.first_name, quote = quote)




@views.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    getforms()
        
    return render_template('logging.html', user=current_user)

@views.route('/logs_maths', methods=['GET', 'POST'])
@login_required
def logs_maths():
    
        
    return render_template('logging_maths.html', user=current_user)




@views.route('/help_bio', methods=['GET', 'POST'])
@login_required
def help_bio():
    
        
    return render_template('help_bio.html', user=current_user, name = current_user.first_name)


@views.route('/help_maths', methods=['GET', 'POST'])
@login_required
def help_maths():
    
        
    return render_template('help_maths.html', user=current_user, name = current_user.first_name)

@views.route('/quiz_maths', methods=['GET', 'POST'])
@login_required
def quiz_maths():
    
        
    return render_template('quiz_maths.html', user=current_user, name = current_user.first_name)


@views.route('/quiz_bio', methods=['GET', 'POST'])
@login_required
def quiz_biology():  
    get_topic()
        
    return render_template('quiz_bio.html', user=current_user, name = current_user.first_name)


@views.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    try:
        print("Hello FUCKING WORK PLEASE ")
        data = json.loads(request.data)
        print(data)
    except ValueError:
        print('Unable to parse JSON data from request.')
    return render_template('questions.html', user=current_user)



@views.route('/call', methods=['GET', 'POST'])
@login_required
def call():


    return render_template("call.html", user = current_user)


