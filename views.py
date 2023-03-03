from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO , send , emit
import os
import json
import numpy
import random
import matplotlib
from more_def import *
from __init__ import *
from models import User
from account import account
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from matplotlib.animation import FuncAnimation
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from flask import Flask, render_template, request, abort








views = Blueprint('views', __name__)

def create():
    acc = account()
    return acc 

acc = create()


@views.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == "POST":
        button1 = request.getParameter("button1");
        print(button1)
    return render_template("main_page.html", user=current_user)

#Home pages for the two account types

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


#Logging method for bio maths and teacher

@views.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    acc.store_logs_database()
        
    return render_template('logging.html', user=current_user)


@views.route('/logs_maths', methods=['GET', 'POST'])
@login_required
def logs_maths():
    acc.get_forms_maths()
        
    return render_template('logging_maths.html', user=current_user)


@views.route('/taught', methods=['GET', 'POST'])
@login_required
def taught():
    acc.log_teaching()
    posts = post.query.all()


    return render_template('teacher_logs.html', user=current_user, posts = posts)



#Getting help 

@views.route('/help_bio', methods=['GET', 'POST'])
@login_required
def help_bio():
    acc.test()
    teacher = acc.get_teacher()
    t_name = teacher[2]
    t_email = teacher[1]
    return render_template('help_bio.html', user=current_user, name = current_user.first_name, teacher_email = t_email,teacher_name = t_name)


@views.route('/help_maths', methods=['GET', 'POST'])
@login_required
def help_maths():
    teacher = acc.get_teacher()
    t_name = teacher[2]
    t_email = teacher[1]
        
    return render_template('help_maths.html', user=current_user, name = current_user.first_name,teacher_email = t_email,teacher_name = t_name)


#Doing questions

@views.route('/quiz_maths', methods=['GET', 'POST'])
@login_required
def quiz_maths():
    acc.get_topic()
        
    return render_template('quiz_maths.html', user=current_user, name = current_user.first_name)


@views.route('/quiz_bio', methods=['GET', 'POST'])
@login_required
def quiz_biology():  
    acc.get_topic()
    

        
    return render_template('quiz_bio.html', user=current_user, name = current_user.first_name)


@views.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    


    return render_template('questions.html', user=current_user)



@views.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():   
    acc.mark_received()


    return render_template('answer.html', user=current_user)






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
            acc.user_image_db(filename)
    return render_template('upload.html', user = current_user)





@views.route('/send', methods=['POST'])
def send():
    # Get the message data from the form
    data = json.loads(request.data)
    print(data)
    recipient = data["recipient"]
    message = data["message"]

    print("hi")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    user = current_user
    sender_id = user.id
    # Save the message to the database
    cursor.execute("""INSERT INTO messages (sender_id, recipient_id, message) VALUES (?, ?, ?)""", 
                      (sender_id, recipient, message))
    conn.commit()
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
    user = current_user
                    # Send any undelivered messages to the user
    messages = acc.get_mess()
    print(messages)
   #Delete the messages from the database
    
 


    return render_template('chat.html', user = current_user, users = users, messages = messages )


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


#Mark questions done by other people
@views.route('/marks', methods =['GET','POST'] )
@login_required
def mark():
    mark = acc.send_answer_to_mark()
    if not mark:
        return render_template('no_mark.html', user = current_user)
    elif mark:
        uservalue = mark[1]
        userid = mark[2]
        return render_template('mark.html', user = current_user,mark_user = uservalue,userid =userid)



@views.route('/stats', methods =['GET','POST'] )
@login_required
def update():
        data1 = acc.get_data(1)
        plot_div1 = acc.draw_graph(data1[0],data1[2],1)

        data2 = acc.get_data(2)
        plot_div2 = acc.draw_graph(data2[0],data2[2],2)

        data3 = acc.get_data(3)
        plot_div3 = acc.draw_graph(data3[0],data3[2],3)

        data4 = acc.get_data(4)
        plot_div4 = acc.draw_graph(data4[0],data4[2],4)

        data5 = acc.get_data(5)
        plot_div5 = acc.draw_graph(data5[0],data5[2],5)

        data6 = acc.get_data(6)
        plot_div6 = acc.draw_graph(data6[0],data6[2],6)

        data7 = acc.get_data(7)
        plot_div7 = acc.draw_graph(data7[0],data7[2],7)

        data8 = acc.get_data(8)
        plot_div8 = acc.draw_graph(data8[0],data8[2],8)
        return render_template('stats.html', user = current_user, plot_div1 = plot_div1, plot_div2=plot_div2,
                              plot_div3 = plot_div3, plot_div4=plot_div4, 
                              plot_div5 = plot_div5, plot_div6=plot_div6,
                              plot_div7 = plot_div7, plot_div8=plot_div8)


@views.route('/statsmaths', methods =['GET','POST'] )
@login_required
def update_maths():
        data1 = acc.get_data_maths(1)
        plot_div1 = acc.draw_graph(data1[0],data1[2],1)

        data2 = acc.get_data_maths(2)
        plot_div2 = acc.draw_graph(data2[0],data2[2],2)

        data3 = acc.get_data_maths(3)
        plot_div3 = acc.draw_graph(data3[0],data3[2],3)

        
        return render_template('stats_maths.html', user = current_user, plot_div1 = plot_div1, plot_div2=plot_div2,
                              plot_div3 = plot_div3)





@views.route('/store', methods=['POST'])
def store():
    
    data = json.loads(request.data)
    print(data)
    time_spent = data["time_spent"]
    print(time_spent)
    acc.get_time(time_spent)
    return render_template("answer.html" , user = current_user )
    



@views.route('/testingthis')
def testthis():
    user = current_user
    data = {'id': user.id}
    return jsonify(data)



@views.route('/choice', methods=['GET','POST'])
@login_required
def choice():

    return render_template("choice.html" , user = current_user )



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