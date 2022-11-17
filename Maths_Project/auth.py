from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user
from student import student, teacher


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                #getting the status to direct the account to their correct home page
                sta = str(user.status)
                print(sta)
                
                if sta == "teacher":
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.teacher_home'))
                elif sta == "student":
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.student_home'))
                        
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.main_page'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        status = request.form.get('status')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. ', category='error')
        elif len(email) < 4:
            flash('Email must be more than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name most be greater than 1 character.', category = 'error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif status == None:
            flash('Please pick a status label.', category = 'error')
        else:
            new_user = User(email=email, first_name=first_name, last_name = last_name, status = status , password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            if status == "teacher":  
                flash('Account created!', category='success')
                return redirect(url_for('views.teacher_home'))
            elif status == "student":
                flash('Account created!', category='success')
                return redirect(url_for('views.student_home'))


            if status == "student":
                stud = student()
            elif status == "teacher":
                teach = teacher()
            stud.test()
    return render_template("sign_up.html", user=current_user)