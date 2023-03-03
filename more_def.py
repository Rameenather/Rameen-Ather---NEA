from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import *
import json
from models import User, post
import random
import sqlite3
from datetime import date , datetime, timedelta
import smtplib
import os
import statistics 
from account import account











def getforms_bio():
    if request.method == 'POST':
        lipids = request.form.get('lipids')
        protein = request.form.get('protein')
        water = request.form.get('water')
        atp = request.form.get('atp')
        Carbohydrates = request.form.get('Carbohydrates')
        dna = request.form.get('dna')
        Cellstructure = request.form.get('cellstructure')
        transportacrossmembrane = request.form.get('transportacrossmembrane')
        cellcycle = request.form.get('cellcycle')
        immunesystem = request.form.get('immunesystem')
        gasexchange = request.form.get('gasexchange')
        digestionandabsorption = request.form.get('digestionandabsorption')
        masstransport = request.form.get('masstransport')
        proteinsynthesis = request.form.get('proteinsynthesis')
        biodiversity = request.form.get('biodiversity')
        geneticdiversity = request.form.get('geneticdiversity')
        photosynthesis = request.form.get('photosynthesis')
        respiration = request.form.get('respiration')
        nitrogencycle = request.form.get('nitrogencycle')
        energyandecosystem = request.form.get('energyandecosystem')
        responsetostimuli = request.form.get('responsetostimuli')
        nervouscoordinationandmuscles = request.form.get('nervouscoordinationandmuscles')
        homeostasis = request.form.get('homeostasis')
        inheritedchange = request.form.get('inheritedchange')
        populationandevolution = request.form.get('populationandevolution')
        populationinecosystems = request.form.get('populationinecosystems')
        geneexpression = request.form.get('geneexpression')
        recombinantDNAtechnology = request.form.get('recombinantDNAtechnology')

        #will be stored in database :D this is temp
        topic = {
            'lipids':lipids,
            'protein':protein,
            'water':water,
            'atp':atp,
            'Carbohydrates':Carbohydrates,
            'dna':dna,
            'Cellstructure':Cellstructure,
            'transportacrossmembrane':transportacrossmembrane,
            'cellcycle':cellcycle,
            'immunesystem':immunesystem,
            'geneexpression':geneexpression

            }
        print(topic)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        user = current_user
        current_date = date.today()
        user_id = user.id

        #insert into topic 1
        cursor.execute("""
        INSERT INTO topic1 (account_id, date_entered, lipid, carbohydrates, protein_and_enzymes, DNA, ATP, Water_and_inorganic_ions) VALUES (?,?,?,?,?,?,?,?)""",
        (user_id, current_date, lipids, Carbohydrates, protein, dna, atp, water))

        #insert into topic 2
        cursor.execute("""
        INSERT INTO topic2 (account_id, date_entered, cell_structure, transport_across_membrane, cell_cycle, immune_system) VALUES (?,?,?,?,?,?)""",
        (user_id, current_date, Cellstructure, transportacrossmembrane, cellcycle, immunesystem))

        #insert into topic 3
        cursor.execute("""
        INSERT INTO topic3 (account_id, date_entered, gas_exchange, digestion_and_absorption, mass_transport) VALUES (?,?,?,?,?)""",
        (user_id, current_date, gasexchange, digestionandabsorption, masstransport))

        #insert into topic 4
        cursor.execute("""
        INSERT INTO topic4 (account_id, date_entered, protein_synthesis, biodiversity, genetic_diversity) VALUES (?,?,?,?,?)""",
        (user_id, current_date, proteinsynthesis, biodiversity, geneticdiversity))

        #insert into topic 5
        cursor.execute("""
        INSERT INTO topic5 (account_id, date_entered, photosynthesis, respiration, nitrogen_cycle, energy_and_ecosystem) VALUES (?,?,?,?,?,?)""",
        (user_id, current_date, photosynthesis, respiration, nitrogencycle, energyandecosystem))

        #insert into topic 6
        cursor.execute("""
        INSERT INTO topic6 (account_id, date_entered, response_to_stimuli, nervous_coordination_and_muscles, homeostasis) VALUES (?,?,?,?,?)""",
        (user_id, current_date, responsetostimuli, nervouscoordinationandmuscles, homeostasis))

        #insert into topic 7
        cursor.execute("""
        INSERT INTO topic7 (account_id, date_entered, inherited_change, population_and_evolution, population_in_ecosystems) VALUES (?,?,?,?,?)""",
        (user_id, current_date, inheritedchange, populationandevolution, populationinecosystems))

        #insert into topic 8
        cursor.execute("""
        INSERT INTO topic8 (account_id, date_entered, gene_expression, recombinant_DNA_technology ) VALUES (?,?,?,?)""",
        (user_id, current_date, geneexpression, recombinantDNAtechnology))

        conn.commit()
        cursor.close()
        conn.close()
        print(topic)
        
def get_forms_maths():
    if request.method == 'POST':
        proof = request.form.get('proof')
        algebraandfunctions = request.form.get('algebraandfunctions')
        coordinategeometry = request.form.get('coordinategeometry')
        squencesandseries = request.form.get('squencesandseries')
        trigonometry = request.form.get('trigonometry')
        exponentialsandlogarithms = request.form.get('exponentialsandlogarithms')
        differentiation = request.form.get('differentiation')
        integration = request.form.get('integration')
        numericalmethods = request.form.get('numericalmethods')
        vectors = request.form.get('vectors')
        quantitiesandunitsinmechanics = request.form.get('quantitiesandunitsinmechanics')
        kinematics = request.form.get('kinematics')
        forcesandnewtonslaws = request.form.get('forcesandnewtonslaws')
        moments = request.form.get('moments')
        statisticalsampling = request.form.get('statisticalsampling')
        datapresentationandinterpretation = request.form.get('datapresentationandinterpretation')
        probability = request.form.get('probability')
        statisticaldistributions = request.form.get('statisticaldistributions')
        statisticalhypothesistesting = request.form.get('statisticalhypothesistesting')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        user = current_user
        current_date = date.today()
        user_id = user.id
        #insert into pure
        cursor.execute("""
        INSERT INTO pure (account_id, date_entered, proof, algebra_and_functions, coordinate_geometry, sequences_and_series, trigonometry, exponentials_and_logarithms, differentiation, integration,) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id, current_date, proof, algebraandfunctions, coordinate_geometry, sequences_and_series, trigonometry, exponentials_and_logarithms,differentiation, integration,numerical_methods))

        #insert into mech
        cursor.execute("""
        INSERT INTO topic1 (account_id, date_entered, vectors, quantities_and_units_in_mechanics, kinematics, forces_and_Newton, moments) VALUES (?,?,?,?,?,?,?)""",
        (user_id, current_date, vectors, quantities_and_units_in_mechanics, kinematics, forces_and_Newton, moments))

        #insert into stats
        cursor.execute("""
        INSERT INTO topic1 (account_id, date_entered, statistical_sampling, data_presentation_and_interpretation, probability, statistical_distributions, statistical_hypothesis) VALUES (?,?,?,?,?,?,?)""",
        (user_id, current_date, statistical_sampling, data_presentation_and_interpretation, probability, statistical_distributions, statistical_hypothesis))


        conn.commit()
        cursor.close()
        conn.close()


def get_questions(topic):
    """Gets the question of the topic the user wants"""

    if os.path.exists('static/questions/q1.png'):
        os.remove('static/questions/q1.png')
        os.remove('static/questions/q1-ans.png')
    if os.path.exists('static/questions/q2.png'):
        os.remove('static/questions/q2.png')
        os.remove('static/questions/q2-ans.png')
    if os.path.exists('static/questions/q3.png'):
        os.remove('static/questions/q3.png')
        os.remove('static/questions/q3-ans.png')
    if os.path.exists('static/questions/q4.png'):
        os.remove('static/questions/q4.png')
        os.remove('static/questions/q4-ans.png')
    if os.path.exists('static/questions/q5.png'):
        os.remove('static/questions/q5.png')
        os.remove('static/questions/q5-ans.png')

    #Emptying both the temp lists from the previous questions stuff
    while(temp_ids != []):
        temp_ids.pop()
    while(temp_list != []):
        temp_list.pop()

    import base64
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    m = cursor.execute (f"""
        SELECT id,question, answer
        FROM questions
        WHERE topic = ?
        """,[topic])
    print(m)
    

    for i in range(5):
        try:
            ran = random.randint(len(m/3))
            for x in m:
                temp_ids.append(x[ran*3])
                rec_test  = x[(ran*3)+1]
                rec_test1 = x[(ran*3) +2]
        

            with open(f'static/q{i}.png','wb') as q:
                q.write(rec_test)

            with open(f'static/q{i}-ans.png','wb') as a:
                a.write(rec_test1)
        except:
            i-=1

    conn.commit()

    user = current_user
    current_date = date.today()
    user_id = user.id
    

    for i in range(5):
        cursor.execute (f"""
            INSERT INTO account_marks (acc_id, qa_id , date_entered) VALUES(?,?,?)""" 
            (user_id,current_date,temp_id[i]))
        conn.commit()
        last_id = cursor.execute("""SELECT questions_done_id
                                    FROM account_marks
                                    ORDER BY DESC limit 1; """).fetchall()
        temp_list.append(last_id)
        conn.commit()
        cursor.execute("""INSERT INTO account_answer(questions_done_id) VALUES (?) """ 
                       (last_id))
        conn.commit()



    conn.commit()
    cursor.close()
    conn.close()

    
def answer_database():
    if request.method == 'POST':
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        q5 = request.form.get('q5')

        listy =[]
        listy.append(q1)
        listy.append(q2)
        listy.append(q3)
        listy.append(q4)
        listy.append(q5)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        user = current_user
        current_date = date.today()
        user_id = user.id

        for i in range(1,5):  
            cursor.execute("""
                INSERT INTO account_answer(acc_id,qa_id,date_entered,marks) VALUES (?,?,?,?)""",
                (user_id,temp_ids[i],current_date,listy[i]))
            conn.commit()
    cursor.close()
    conn.close()


def get_topic():
    if request.method == 'POST':
        topic = request.form.get('sclt2')
        if topic == None:
            quick_fire_five()
        else:
            get_questions(topic)
            
        print(topic)
    return topic 





def send_email():
    """Queries emails and sends an email to all the student 
    acc with there topic as a reminder to revise"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    status = "student"
    cursor.execute("""
        SELECT email, first_name
        FROM user
        WHERE status = ?""",[status])

    data = cursor.fetchall()

    my_email = "testingmycode1@outlook.com"
    password  = "Street4."
    send_email = "rameenather22@gmail.com"

    current_time = datetime.now()
    if current_time.hour == 18:
        for i in data:
            send_an_email(my_email,password,i[0],"topic",i[1])

    #Login email detail and sending email detail

    conn.commit()
    cursor.close()
    conn.close()




#initialize connection to our email server, we will use Outlook here
def send_an_email(my_email,password,send_email,topic, name):

    """Sends an email"""

    with smtplib.SMTP('smtp-mail.outlook.com', port='587') as smtp:
        smtp.ehlo()  # send the extended hello to our server
        smtp.starttls()  # tell server we want to communicate with TLS encryption
        smtp.login(user = my_email, password = password)  # login to our email server
        smtp.sendmail(from_addr = my_email,
                      to_addrs = send_email,
                      msg = f"""Subject:Email from maths/Biology revision \n\n {name} Hi its time to revise {topic} to make sure you get an A*""") #The email message. 
    print("email success")

    

def get_teacher():
    import random
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    status = "teacher"
    cursor.execute("""
        SELECT email, first_name
        FROM user
        WHERE status = ?""",[status])

    teach = random.choose(cursor)
    print(teach)

    conn.commit()
    cursor.close()
    conn.close()


def quick_fire_five():
    import random
    conn.sqlite3.connect('database.db')
    cursor = conn.cursor()
    m = cursor.execute("""
        SELECT id
        FROM question
    """)
    data = cursor.fetchall()
    conn.commit()
    

    for i in 5:
        num = random.choice(data)
        temp_id.append(num)
        q = cursor.execute("""
                SELECT id, question, answer
                FROM question
                WHERE id = num
                """)
      
        for x in q:
            rec_data = x[1]
            rec_data1 = x[2]

        with open(f'static/q{i}.png','wb') as f:
            f.write(rec_data)

        with open(f'static/q{i}-ans.png','wb') as a:
            a.write(rec_data1)
    

        conn.commit()
        
    user = current_user
    current_date = date.today()
    user_id = user.id

    for i in range(5):
        cursor.execute (f"""
            INSERT INTO account_answer (acc_id, qa_id , date_entered) VALUES(?,?,?)""" 
            (user_id,current_date,temp_id[i]))
    conn.commit()
    cursor.close()
    conn.close()


def stats_logs_bio():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    user = current_user
    current_date = date.today()
    user_id = user.id

    topic1 = cursor.execute (f"""
        SELECT lipid, carbohydrates, protein_and_enzymes, dna, atp, Water_and_inorganic_ions
        FROM topic1
        WHERE account_id = ?
        """,[user_id])
         
    topic2 = cursor.execute (f"""
        SELECT cell_structure, transport_across_membrane ,cell_cycle, immune_system
        FROM topic2
        WHERE account_id = ?
        """,[user_id])
         
    topic3 = cursor.execute (f"""
        SELECT gas_exchange, digestion_and_absorption, mass_transport
        FROM topic3
        WHERE account_id = ?
        """,[user_id])

    topic4 = cursor.execute (f"""
        SELECT protein_synthesis, biodiversity, genetic_diversity
        FROM topic4
        WHERE account_id = ?
        """,[user_id])

    topic5 = cursor.execute (f"""
        SELECT photosynthesis, respiration, nitrogen_cycle, energy_and_ecosystem
        FROM topic5
        WHERE  account_id = ?
        """,[user_id])

    topic6 = cursor.execute (f"""
        SELECT homeostasis,nervous_coordination_and_muscles, response_to_stimuli
        FROM topic6
        WHERE  account_id = ?
        """,[user_id])

    topic7 = cursor.execute (f"""
        SELECT inherited_change, population_and_evolution, population_in_ecosystems
        FROM topic7
        WHERE  account_id = ?
        """,[user_id])

    topic8 = cursor.execute (f"""
        SELECT gene_expression, recombinant_DNA_technology
        FROM topic8
        WHERE  account_id = ?
        """,[user_id])

    t1 = topic1.fetchall()
    results1 = get_stats(t1)

    t2 = topic2.fetchall()
    results2 = get_stats(t2)

    t3 = topic3.fetchall()
    results3 = get_stats(t3)

    t4 = topic4.fetchall()
    results4 = get_stats(t4)

    t5 = topic5.fetchall()
    results5 = get_stats(t5)
    t6 = topic6.fetchall()
    results6 = get_stats(t6)
    t7 = topic7.fetchall()
    results7 = get_stats(t7)
    t8 = topic8.fetchall()
    results8 = get_stats(t8)



    

    


    conn.commit()
    cursor.close()
    conn.close()

def get_stats(t1):
    t11 = 0
    t12 = 0
    t13 = 0
    t14 = 0
    t15 = 0
    t16 = 0
    
    print(t1)
    for row in t1:
        t11 += row[0]
        t12 += row[1]
        t13 += row[2]
        t14 += row[3]
        t15 += row[4]
        t16 += row[5]
        print(row)
    tempy = []
    tempy.append(t11)
    tempy.append(t12)
    tempy.append(t13)
    tempy.append(t14)
    tempy.append(t15)
    tempy.append(t16)

    highest1 = None
    for i in tempy:
        if tempy[i+1] > tempy[i]:
            highest = tempy[i+1]
        else:
            highest = temp[i]


    temp1 = statistics.stdev(tempy)
    return temp1

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email 
        FROM user""")
    users = cursor.fetchall()
    return jsonify(users)


    conn.commit()
    cursor.close()
    conn.close()


def account_answers():
    if request.method == 'POST':
        image_input = request.form.get('inputGroupFile02')
        print(image_input)

def teach_logs():
    if request.method == "POST":
        student_email = request.form.get("student_email")
        student_user = request.form.get("student_name")
        taught = request.form.get("taught")
        

        if not taught:
            flash("You have not entered what you taught",category="error")
        else:
            post_ = post(student_email = student_email,student_name= student_user,taught = taught, teacher = current_user.id )
            db.session.add(post_)
            db.session.commit()
            flash('Teaching log added!' , category= 'success')
           


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def user_image_db(filename):
    """Inserts images uploaded by the user into the database"""
    with open(f'static/user_ans/{filename}' , 'rb') as u:
        image_ans = u.read()


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO account_answer(question_done_id, user_answers) VALUES (?,?)""",
        (1,image_ans))
    


    conn.commit()
    cursor.close()
    conn.close()

    os.remove(f"static/user_ans/{filename}")


def send_email():
        """Queries emails and sends an email to all the student 
        acc with a topic as a reminder to revise"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        status = "student"
        my_email = "testingmycode1@outlook.com"
        password  = "SomethingSomething12"
        now = datetime.now()
        date_week = now-timedelta(7)
        date = date_week.date()
        print(date_week)
        with open("email.txt") as email_points:  
            email_text = email_points.readlines()


        cursor.execute("""
                SELECT id, email, first_name
                FROM user
                WHERE status = ?""",[status])

        email_data = cursor.fetchall()
        print(email_data)
        for person in email_data:
            email_text = random.choice(email_text)
            cursor.execute("""
                SELECT email,first_name, question_done_id, acc_id, marks, topic, first_name
                FROM account_marks, user
                WHERE account_marks.acc_id = ? and account_marks.date_entered = ?""",[person[0]][date])
            questions_done_week_ago = cursor.fetchone()
            cursor.commit()

            if questions_done_week_ago == None:
                start_text = "Your reminder to revise"
                topic = None
                more_text = " "

            else:
                start_text = "You did questions a week ago on "
                topic = questions_done_week_ago[5]
                more_text = f"and you got {person[4]} marks on it. Want to try some more?"

            self.send_an_email(my_email,password,person[1],person[2],email_text,start_text, more_text)
                

        #Login email detail and sending email detail

        conn.commit()
        cursor.close()
        conn.close()

def send_an_email(my_email,password,send_email, name,text, type, topic, more_text):

        """Sends an email"""

        with smtplib.SMTP('smtp-mail.outlook.com', port='587') as smtp:
            smtp.ehlo()  # send the extended hello to our server
            smtp.starttls()  # tell server we want to communicate with TLS encryption
            smtp.login(user = my_email, password = password)  # login to our email server
            smtp.sendmail(from_addr = my_email,
                          to_addrs = send_email,
                          #The email message.
                          msg = f"""Subject:Email from maths/Biology revision \n\n {name} Hi {type} {topic} {more_text}  \n {text}""")
                          
        print("email success")