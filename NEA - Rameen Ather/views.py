from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO , send , emit
from __init__ import *
import json
from models import User
import random
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from werkzeug.utils import secure_filename
from account import account



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
    #getforms_bio()
    acc.store_logs_database()
        
    return render_template('logging.html', user=current_user)

@views.route('/logs_maths', methods=['GET', 'POST'])
@login_required
def logs_maths():
    
        
    return render_template('logging_maths.html', user=current_user)




@views.route('/help_bio', methods=['GET', 'POST'])
@login_required
def help_bio():
    acc.test()
        
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
    

        
    return render_template('quiz_bio.html', user=current_user, name = current_user.first_name, list_of_ids = list_of_q_ids)


@views.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    


    return render_template('questions.html', user=current_user)


@views.route('/ProcessorUserInfo/<string:s>', methods = ["POST"])
def ProcessorUserInfo(s):
    
    totaltime = json.loads(s)
    timetaken = totaltime
    print()
    print(timetaken)
    print("provlmefss")
    return render_template('home.html', user = current_user)



@views.route('/call', methods=['GET', 'POST'])
@login_required
def call():
    

    
    return render_template("fuck.html", user = current_user)

@views.route('/testing', methods=['POST'])
def test():
    import os
    from dotenv import load_dotenv
    from flask import Flask, render_template, request, abort
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VideoGrant



    load_dotenv()
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
    twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

    TWILIO_ACCOUNT_SID = "AC79f8996e6a9fa718d8b9a829ff4a6788"
    TWILIO_API_KEY_SID = 'SKb051122900aab1d1d1bc409c30686115'
    TWILIO_API_KEY_SECRET = 'GW8fHqPmb409YsNLdOC5JplxbQwfOu4t'

    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))

    return {'token': token.to_jwt().decode()}


@views.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():



    return render_template('answer.html', user=current_user)


@views.route('/taught', methods=['GET', 'POST'])
@login_required
def taught():
    teach_logs()
    posts = post.query.all()


    return render_template('teacher_logs.html', user=current_user, posts = posts)




@views.route('/uploadimage', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('upload.html', user = current_user)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('upload.html', user = current_user)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            print(file)
            file.save(os.path.join('static/user_ans', filename))
            user_image_db(filename)
    return render_template('upload.html', user = current_user)





@views.route('/send', methods=['POST'])
def send():
    # Get the message data from the form
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    
    print(sender,message,recipient)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    user = current_user
    sender_id = user.id
    # Save the message to the database
    cursor.execute("""INSERT INTO messages (sender_id, recipient_id, message) VALUES (?, ?, ?)""", 
                      (sender_id, recipient, message))
    conn.commit()

    socketio.emit('receive message', {'sender': sender, 'recipient': recipient, 'message': message}, room=recipient)
    
    # Get the recipient's connection from the list of connected users
    #recipient_connection = connected_users.get(recipient)
    #if recipient_connection:
        # Send the message to the recipient
     #   recipient_connection.emit('message', message)
    cursor.close()
    conn.close()

    return 'Message sent!'

@views.route('/chat', methods =['GET','POST'] )
@login_required
def chat():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, email FROM user''')
    users = cursor.fetchall()

    return render_template('chat.html', user = current_user, users = users)


@views.route('/users')
def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, email FROM user''')
    users = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return users


@views.route('/marks', methods =['GET','POST'] )
@login_required
def mark():
    acc.send_answer_to_mark()

    return render_template('mark.html', user = current_user,)



