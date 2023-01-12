from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import db ,ALLOWED_EXTENSIONS 
from datetime import date , datetime
from models import User, post
import os
import csv
import json
import numpy
import base64
import random
import smtplib
import sqlite3
import statistics 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation









class account:
    #student account
    def __init__(self):
        self.ids = []
        self.temp = 0 
        self.topic = None
        self.marking = 0

    def test(self):
        print("hello test :P")
        user = current_user
        print(user.id)


    def clear_all(self):
        user = current_user
        if os.path.exists(f'static/questions/{user.id}q1.png'):
            os.remove(f'static/questions/{user.id}q1.png')
            os.remove(f'static/questions/{user.id}q1-ans.png')
        if os.path.exists(f'static/questions/{user.id}q2.png'):
            os.remove(f'static/questions/{user.id}q2.png')
            os.remove(f'static/questions/{user.id}q2-ans.png')
        if os.path.exists(f'static/questions/{user.id}q3.png'):
            os.remove(f'static/questions/{user.id}q3.png')
            os.remove(f'static/questions/{user.id}q3-ans.png')
        if os.path.exisfts(f'static/questions/{user.id}q4.png'):
            os.remove(f'static/questions/{user.id}q4.png')
            os.remove(f'static/questions/{user.id}q4-ans.png')
        if os.path.exists(f'static/questions/{user.id}q5.png'):
            os.remove(f'static/questions/{user.id}q5.png')
            os.remove(f'static/questions/{user.id}q5-ans.png')

        while(self.ids != []):
            self.ids.pop()
        self.temp = 0

    def questions(self,topic):
        """Gets the question of the topic the user wants"""

        #clears all instances of previous questions 
        clear_all()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute (f"""
            SELECT id,question, answer
            FROM questions
            WHERE topic = ?
            """,[topic])
        print(m)
        user = current_user

        for i in range(5):
            try:
                ran = random.randint(len(m/3))
                for x in m:
                    self.ids.append(x[ran*3])
                    rec_test  = x[(ran*3)+1]
                    rec_test1 = x[(ran*3) +2]
        

                with open(f'static/questions/{user.id}q{i}.png','wb') as q:
                    q.write(rec_test)

                with open(f'static/questions/{user.id}q{i}-ans.png','wb') as a:
                    a.write(rec_test1)
            except:
                i-=1

        conn.commit()

        user = current_user
        current_date = date.today()
        user_id = user.id
    
        self.temp = cursor.execute("""SELECT questions_done_id
                                        FROM account_marks
                                        ORDER BY DESC limit 1; """).fetchall()
        self.temp += 1 
        conn.commit()
        for i in range(5):
            cursor.execute (f"""
                INSERT INTO account_marks (acc_id, qa_id , date_entered) VALUES(?,?,?)""" 
                (user_id,current_date,self.ids[i]))
            conn.commit()
            last_id = cursor.execute("""SELECT questions_done_id
                                        FROM account_marks
                                        ORDER BY DESC limit 1; """).fetchall()
            conn.commit()
            cursor.execute("""INSERT INTO account_answer(questions_done_id) VALUES (?) """ 
                           (self.temp))
            conn.commit()


        cursor.close()
        conn.close()


    def quick_fire_five():
        """Picks 5 questions randomly for the user to do"""

        clear_all()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute("""
            SELECT id
            FROM question
        """)
        data = cursor.fetchall()
        conn.commit()
    

        for i in 5:
            num = random.choice(data)
            self.ids.append(num)
            q = cursor.execute("""
                    SELECT id, question, answer
                    FROM question
                    WHERE id = num
                    """)
      
            for x in q:
                rec_data = x[1]
                rec_data1 = x[2]

            with open(f'static/questions/{user.id}q{i}.png','wb') as f:
                f.write(rec_data)

            with open(f'static/questions/{user.id}q{i}-ans.png','wb') as a:
                a.write(rec_data1)
    

            conn.commit()
        
        user = current_user
        current_date = date.today()
        user_id = user.id

        for i in range(5):
            cursor.execute (f"""
                INSERT INTO account_answer (acc_id, qa_id , date_entered) VALUES(?,?,?)""" 
                (user_id,current_date,self.ids[i]))
        conn.commit()
        cursor.close()
        conn.close()


    def mark_scheme(self,topic):
        """Selects answers with the topic wanted (might change)"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute ("""
        SELECT question 
        FROM questions
        WHERE topic = topic
        """)
        

        conn.commit()
        cursor.close()
        conn.close()
        return m

    def enter_answers():
        pass

    def send_answer_to_mark():
        pass

    def mark_received():
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
                    (user_id,self.ids[i],current_date,listy[i]))
                conn.commit()
            cursor.close()
            conn.close()

    def send_email(self):
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
                send_an_email(my_email,password,i[0],i[1])

        #Login email detail and sending email detail

        conn.commit()
        cursor.close()
        conn.close()

    def send_an_email(self,my_email,password,send_email, name):

        """Sends an email"""

        with smtplib.SMTP('smtp-mail.outlook.com', port='587') as smtp:
            smtp.ehlo()  # send the extended hello to our server
            smtp.starttls()  # tell server we want to communicate with TLS encryption
            smtp.login(user = my_email, password = password)  # login to our email server
            smtp.sendmail(from_addr = my_email,
                          to_addrs = send_email,
                          msg = f"""Subject:Email from maths/Biology revision \n\n {name} Hi its time to revise {self.topic} to make sure you get an A*""") #The email message. 
        print("email success")

    def help():
        pass

    def store_logs_database(self):
        """Stores the logs entered to the database"""

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
       


    def get_forms_maths(self):
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
        



    def get_teacher(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        status = "teacher"
        cursor.execute("""
            SELECT id
            FROM user
            WHERE status = ?""",[status])

        teach = random.choose(cursor)
        print(teach)

        conn.commit()

        teacher_date = cursor.execute("""
            SELECT email, first_name
            FROM user
            WHERE id = ?""" ,[teach]).fetchall()

        cursor.close()
        conn.close()

    def get_subject_quiz(self):
       pass

    def get_topic(self):
        if request.method == 'POST':
            self.topic = request.form.get('sclt2')
            if self.topic == None:
                quick_fire_five()
            else:
                questions(self.topic)
            
            print(topic)

    def user_image_db(self,filename):
        """Inserts images uploaded by the user into the database"""
        with open(f'static/user_ans/{filename}' , 'rb') as u:
            image_ans = u.read()

            #here123
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO account_answer(question_done_id, user_answers) VALUES (?,?)""",
            (self.temp,image_ans))
        conn.commit()
        cursor.close()
        conn.close()

        os.remove(f"static/user_ans/{filename}")

    def get_data(self,num):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        user = current_user
        user_id = user.id

        mean = []
        stdev = []
        topics = []

        if num == 1:

            cursor.execute (f"""
                SELECT lipid, carbohydrates, protein_and_enzymes, dna, atp, Water_and_inorganic_ions
                FROM topic1
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])
                list_2d[4].append(row[4])
                list_2d[5].append(row[5])
        
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)


        elif num == 2:
            cursor.execute (f"""
                SELECT cell_structure, transport_across_membrane, cell_cycle, immune_system
                FROM topic2
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])

            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

        elif num == 3:
            cursor.execute (f"""
                SELECT gas_exchange, digestion_and_absorption, mass_transport
                FROM topic3
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])

            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

        elif num == 4:
            cursor.execute (f"""
                SELECT protein_synthesis, biodiversity, genetic_diversity
                FROM topic4
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])

            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)
        
        elif num == 5:
            cursor.execute (f"""
                SELECT photosynthesis, respiration, nitrogen_cycle, energy_and_ecosystem
                FROM topic5
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])

            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

        elif num == 6:
            cursor.execute (f"""
                SELECT response_to_stimuli, nervous_coordination_and_muscles, homeostasis
                FROM topic6
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])

            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

        elif num == 7:
            cursor.execute (f"""
                SELECT inherited_change, population_and_evolution, population_in_ecosystems
                FROM topic7
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

        elif num == 8:
            cursor.execute (f"""
                SELECT gene_expression, recombinant_DNA_technology
                FROM topic8
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
            
            for i in range(len(list_2d)):
                mean.append(statistics.mean(list_2d[i]))

            for i in range(len(list_2d)):
                stdev.append(round(statistics.stdev(list_2d[i]),2))

            
            topics = [i[0] for i in cursor.description]
            return (mean,stdev,topics)

    

    

    def draw_graph(self, x, y,num ):
        """Takes data input and displays it as a graph"""
            fig = px.bar(x=x, y=y, title=f'Mean logs for topic {num}')
        
    # Display the graph on a website
            fig.update_layout(xaxis_title='Topics',
                              yaxis_title='Mean logs')
            plot_div = fig.to_html(full_html = False)

        
            return plot_div



    



class teacher():
    #Teacher account

    def teach(self):
        pass

    def log_teaching():
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
           

    def quick_fire_five():
        pass

    def questions():
        pass

    def mark_scheme():
        pass
    
    def enter_answers():
        pass

    def send_answer_to_mark():
        """finds a accounts answers to mark"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_for_marking
            FROM account_answer
            """)

        questions_to_mark = random.choice(cursor)

        conn.commit()
        m = cursor.execute("""
            SELECT user_answers
            FROM account_answer
            WHERE id_for_marking = ?""",
            [questions_to_mark])
        
        for x in m:
            rec_data = x
            with open(f'static/marking/mark{x}.png','wb') as q:
                        q.write(rec_data)


        conn.commit()
        cursor.close()
        conn.close()


    def mark_recieved():
        pass 

    def add_points():
        pass
