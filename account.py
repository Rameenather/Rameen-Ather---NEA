from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import date , datetime, timedelta
from __init__ import db, ALLOWED_EXTENSIONS 
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
    #account
    def __init__(self):
        self.__current_question_ids = []
        self.__last_question_done_id = 0 
        self.__current_question_done_ids = []
        self.marking = 0
        self.__topic = None
        

    def test(self):
        print("hello test :P")
        user = current_user
        print(user.id)
    #for question ids    
    def get_current_q_ids(self):
        return self.__current_question_ids

    def add_current_q_ids(self,id):
        self.__current_question_ids.append(id)

    def del_current_q_ids(self):
        self.__current_question_ids = []

     #for question done ids       
    def get_current_q_done_ids(self):
        return self.__current_question_done_ids

    def add_current_q_done_ids(self,id):
        self.__current_question_done_ids.append(id)

    def del_current_q_done_ids(self):
        self.__current_question_done_ids = []

    #for the last question done id in the database
    def get_last_question_id(self):
        return self.__last_question_done_id

    def set_last_question(self,id):
        self.__last_question_done_id = id

    def add_last_question(self,add):
        self.__last_question_done_id+=add

    def set_topic(self,topic):
       self.__topic = topic

    def _get_topic(self):
        return self.__topic

    def clear_all(self):
        user = current_user
        if os.path.exists(f'static/questions/q{user.id}0.png'):
            os.remove(f'static/questions/q{user.id}0.png')
            os.remove(f'static/questions/q{user.id}0-ans.png')
        if os.path.exists(f'static/questions/q{user.id}1.png'):
            os.remove(f'static/questions/q{user.id}1.png')
            os.remove(f'static/questions/q{user.id}1-ans.png')
        if os.path.exists(f'static/questions/q{user.id}2.png'):
            os.remove(f'static/questions/q{user.id}2.png')
            os.remove(f'static/questions/q{user.id}2-ans.png')
        if os.path.exists(f'static/questions/q{user.id}3.png'):
            os.remove(f'static/questions/q{user.id}3.png')
            os.remove(f'static/questions/q{user.id}3-ans.png')
        if os.path.exists(f'static/questions/q{user.id}4.png'):
            os.remove(f'static/questions/q{user.id}4.png')
            os.remove(f'static/questions/q{user.id}4-ans.png')

        self.del_current_q_ids()
        self.del_current_q_done_ids()
        self.set_last_question(0)



    def questions(self,topic):
        """Gets the question of the topic the user wants"""

        #clears all instances of previous questions 
        self.clear_all()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute (f"""
            SELECT id,question, answer
            FROM questions
            WHERE topic = ?
            ORDER BY RANDOM()
            """,[topic])
        m = m.fetchmany(5)
        user = current_user

        for i in range(5):
            try:
                self.add_current_q_ids(m[i][0])
                with open(f'static/questions/q{user.id}{i}.png','wb') as q:
                    q.write(m[i][1])
                print("tried" )

                with open(f'static/questions/q{user.id}{i}-ans.png','wb') as a:
                    a.write(m[i][2])
            except:
                i-=1
        print(self.get_current_q_ids())
        conn.commit()

        user = current_user
        current_date = date.today()
        user_id = user.id
    
        cursor.execute("""SELECT question_done_id
                          FROM acc_mark
                          ORDER BY question_done_id DESC limit 1; """)
        last_id = cursor.fetchone()
        print(self.get_last_question_id())       

        if last_id == None:
            self.last_question_id = 1
        else:
            
            self.add_last_question(last_id[0] + 1)
            print(self.get_last_question_id())
            
        conn.commit()
        self.add_current_q_ids(self.get_last_question_id())

        for i in range(5):
            print(self.get_current_q_ids())
            cursor.execute("""INSERT INTO acc_mark (question_done_id, acc_id, qa_id , date_entered) VALUES(?,?,?,?)""" ,
                (self.get_last_question_id(),user_id,self.get_current_q_ids()[i],current_date))
            self.add_last_question(1)
            self.add_current_q_ids(self.get_last_question_id())
            conn.commit()



        cursor.close()
        conn.close()

    



    def quick_fire_five(self):
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
    
        self.clear_all()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute (f"""
            SELECT id,question, answer
            FROM questions
            ORDER BY RANDOM()
            """)

        m = m.fetchmany(5)

        user = current_user

        for i in range(5):
            try:
                self.add_current_q_ids(m[i][0])
                with open(f'static/questions/q{user.id}{i}.png','wb') as q:
                    q.write(m[i][1])

                with open(f'static/questions/q{user.id}{i}-ans.png','wb') as a:
                    a.write(m[i][2])
            except:
                i=-1
            conn.commit()

        user = current_user
        current_date = date.today()
        user_id = user.id

        cursor.execute("""SELECT *
                          FROM acc_marks
                          ORDER BY question_done_id DESC limit 1; """)
        temp = cursor.fetchone()

        if temp == None:
            self.set_last_question(1)
        else:
            self.set_last_question(temp[0])

        self.add_current_q_ids(self.get_last_question_id())
        conn.commit()
        for i in range(5):
            print(self.get_current_q_ids())
            cursor.execute("""INSERT INTO acc_marks (question_done_id, acc_id, qa_id , date_entered) VALUES(?,?,?,?)""" ,
                (self.get_last_q_id(),user_id,self.get_current_q_ids()[i],current_date))
            self.set_last_question(1)
            self.add_current_q_ids(self.get_last_question_id())
            conn.commit()



    def mark_received(self):
        if request.method == 'POST':
            q1 = request.form.get('q1')
            q2 = request.form.get('q2')
            q3 = request.form.get('q3')
            q4 = request.form.get('q4')
            q5 = request.form.get('q5')

            print(q1,q2,q3)
            mark_recieved =[]
            mark_recieved.append(q5)
            mark_recieved.append(q4)
            mark_recieved.append(q3)
            mark_recieved.append(q2)
            mark_recieved.append(q1)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            user = current_user
            current_date = date.today()
            user_id = user.id

            cursor.execute("""SELECT question_done_id
                          FROM acc_mark
                          ORDER BY question_done_id DESC limit 5; """)
            temp = cursor.fetchall()
            print(temp)
            print(mark_recieved)

            for i in range(0,5): 
                cursor.execute(f"""
                    UPDATE acc_mark
                    SET marks = ?
                    WHERE acc_id = ? and question_done_id = ?
                """,[mark_recieved[i],user_id,temp[i][0]])
                conn.commit()
            cursor.close()
            conn.close()


    


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
            
       


    def get_forms_maths(self):
        if request.method == 'POST':
            proof = request.form.get('proof')
            algebraandfunctions = request.form.get('algebraandfunctions')
            coordinategeometry = request.form.get('coordinategeometry')
            sequencesandseries = request.form.get('squencesandseries')
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
            INSERT INTO pure (account_id, date_entered, proof, algebra_and_functions, coordinate_geometry, sequences_and_series, trigonometry, exponentials_and_logarithms, differentiation, integration,numerical_methods) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (user_id, current_date, proof, algebraandfunctions, coordinategeometry, sequencesandseries, trigonometry, exponentialsandlogarithms,differentiation, integration,numericalmethods))

            #insert into mech
            cursor.execute("""
            INSERT INTO mech (account_id, date_entered, vectors, quantities_and_units_in_mechanics, kinematics, forces_and_Newton’s_laws, moments) VALUES (?,?,?,?,?,?,?)""",
            (user_id, current_date, vectors, quantitiesandunitsinmechanics, kinematics, forcesandnewtonslaws, moments))

            #insert into stats
            cursor.execute("""
            INSERT INTO stats (account_id, date_entered, statistical_sampling, data_presentation_and_interpretation, probability, statistical_distributions, statistical_hypothesis_testing) VALUES (?,?,?,?,?,?,?)""",
            (user_id, current_date, statisticalsampling, datapresentationandinterpretation, probability, statisticaldistributions, statisticalhypothesistesting))


            conn.commit()
            cursor.close()
            conn.close()
        



    def get_teacher(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        status = "teacher"
        cursor.execute("""
            SELECT id, email, first_name, last_name
            FROM user
            WHERE status = ?
            ORDER BY RANDOM()""",[status])

        teach = cursor.fetchone()
        print(teach)


        conn.commit()
        cursor.close()
        conn.close()
        return teach


    

    def get_topic(self):
        if request.method == 'POST':
            self.__topic = request.form.get('slct2')
            if self.__topic == None:
                self.quick_fire_five()
            else:
                print("works")
                self.questions(self.__topic)
            
            print(self.__topic)


    def user_image_db(self,filename):
        """Inserts images uploaded by the user into the database"""
        with open(f'static/user_ans/{filename}' , 'rb') as u:
            image_ans = u.read()

            #here123
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO account_answer(question_done_id, user_answers) VALUES (?,?)""",
            (self.get_last_question_id()-1,image_ans))
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

            cursor.execute("""
                 SELECT AVG(lipid), AVG(carbohydrates), AVG(protein_and_enzymes), AVG(dna), AVG(atp), AVG(Water_and_inorganic_ions)
                 FROM topic1
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()

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
            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 2:

            cursor.execute("""
                 SELECT AVG(cell_structure), AVG(transport_across_membrane), AVG(cell_cycle), AVG(immune_system)
                 FROM topic2
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()

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

            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 3:

            cursor.execute("""
                 SELECT AVG(gas_exchange), AVG(digestion_and_absorption), AVG(mass_transport)
                 FROM topic3
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()


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

            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 4:

            cursor.execute("""
                 SELECT AVG(protein_synthesis), AVG(biodiversity), AVG(genetic_diversity)
                 FROM topic4
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()
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


            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)
        
        elif num == 5:

            cursor.execute("""
                 SELECT AVG(photosynthesis), AVG(respiration), AVG(nitrogen_cycle), AVG(energy_and_ecosystem)
                 FROM topic5
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()
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


            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 6:

            cursor.execute("""
                 SELECT AVG(response_to_stimuli), AVG(nervous_coordination_and_muscles), AVG(homeostasis)
                 FROM topic6
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()
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

            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 7:

            cursor.execute("""
                 SELECT AVG(inherited_change), AVG(population_and_evolution), AVG(population_in_ecosystems)
                 FROM topic7
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()
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
            

            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

        elif num == 8:

            cursor.execute("""
                 SELECT AVG(gene_expression), AVG(recombinant_DNA_technology)
                 FROM topic8
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()
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

            try:
                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,topics)

    def get_data_maths(self,num):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        user = current_user
        user_id = user.id

        mean = []
        stdev = []
        topics = []

        if num == 1:

            cursor.execute("""
                 SELECT AVG(proof), AVG(algebra_and_functions), AVG(coordinate_geometry), AVG(sequences_and_series), AVG(trigonometry), AVG(exponentials_and_logarithms), AVG(differentiation), AVG(integration), AVG(numerical_methods)
                 FROM pure
                 WHERE account_id =?
            """,[user_id])
            average = cursor.fetchall()

            cursor.execute (f"""
                SELECT proof, algebra_and_functions, coordinate_geometry, sequences_and_series, trigonometry, exponentials_and_logarithms,differentiation,integration,numerical_methods
                FROM pure
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[],[],[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])
                list_2d[4].append(row[4])
                list_2d[5].append(row[5])
                list_2d[6].append(row[6])
                list_2d[7].append(row[7])
                list_2d[8].append(row[8])
            try:

                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,None)

        elif num == 2:

            cursor.execute (f"""
                SELECT AVG(vectors), AVG(quantities_and_units_in_mechanics),AVG(kinematics), AVG(forces_and_Newton’s_laws), AVG(moments)
                FROM mech
                WHERE account_id = ?
                """,[user_id])
            average = cursor.fetchall()

            cursor.execute (f"""
                SELECT vectors, quantities_and_units_in_mechanics, kinematics, forces_and_Newton’s_laws, moments
                FROM mech
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])
                list_2d[4].append(row[4])
            try:
        
                for i in range(len(list_2d)):
                    mean.append(statistics.mean(list_2d[i]))


                topics = [i[0] for i in cursor.description]
                return (average,stdev,topics)
            except:
                return (0,0,None)


        elif num == 3:

            cursor.execute (f"""
                SELECT AVG(statistical_sampling), AVG(data_presentation_and_interpretation),AVG(probability), AVG(statistical_distributions), AVG(statistical_hypothesis_testing)
                FROM stats
                WHERE account_id = ?
                """,[user_id])
            average = cursor.fetchall()

            cursor.execute (f"""
                SELECT statistical_sampling, data_presentation_and_interpretation, probability, statistical_distributions, statistical_hypothesis_testing
                FROM stats
                WHERE account_id = ?
                """,[user_id])
            topic_1 = cursor.fetchall()
            list_2d = [[],[],[],[],[]]

            for row in topic_1:
                list_2d[0].append(row[0])
                list_2d[1].append(row[1])
                list_2d[2].append(row[2])
                list_2d[3].append(row[3])
                list_2d[4].append(row[4])
            try:
       

                for i in range(len(list_2d)):
                    stdev.append(round(statistics.stdev(list_2d[i]),2))

                topics = [i[0] for i in cursor.description]
                return (mean,stdev,topics)
            except:
                return (0,0,None)


    def get_topic_low(self):

        lowest = []
        for i in range(1,9):
            topic1 = self.get_data(i)
            print(topic1)
            lowest_topic = topic1[2][0]
            for i in range(len(topic1[0]) - 1):
                    if (list(topic1[0][i]) < list(topic1[0][i+1])):
                        print(topic1[0][i])
                        lowest_topic = topic1[2][i]
                   
            print(lowest_topic)
            lowest.append(lowest_topic)

           


    
    def get_time(self,time):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        user = current_user
        user_id = user.id
        for i in range(5):
            cursor.execute("""
                INSERT INTO time_taken (question_done_id, time) VALUES (?,?)""",
                (self.get_current_q_ids()[i], time))
            conn.commit()

        conn.commit()
        cursor.close()
        conn.close()


    def draw_graph(self, x, y,num ):
        """Takes data input and displays it as a graph"""
        fig = px.bar(x=x, y=y, title=f'Mean logs for topic {num}')
        
    # Display the graph on a website
        fig.update_layout(xaxis_title='Topics',
                              yaxis_title='Mean logs')
        plot_div = fig.to_html(full_html = False)

        
        return plot_div



    



    def log_teaching(self):
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
           

    def send_answer_to_mark(self):
        """finds a accounts answers to mark"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        user = current_user
        cursor.execute("""
            SELECT id, acc_mark.question_done_id, user.email
            FROM account_answer, acc_mark , user
            WHERE account_answer.question_done_id = acc_mark.question_done_id
            ORDER BY RANDOM()
            """)

        questions_to_mark = cursor.fetchone()

        if questions_to_mark == None:
            return (False)

        else:

            conn.commit()
        
            m = cursor.execute("""
                SELECT acc_mark.question_done_id, user_answers
                FROM account_answer, acc_mark, user
                WHERE user.id = ? and acc_mark.question_done_id = ?""",
                [questions_to_mark[0],questions_to_mark[1]])

            ans_images = m.fetchall()
            for x in range(len(ans_images)):
                rec_data = ans_images[x][1]
                with open(f'static/marking/mark{user.id}{x}.png','wb') as q:
                            q.write(rec_data)

            return (True,questions_to_mark[2],questions_to_mark[0])
        conn.commit()
        cursor.close()
        conn.close()





    def get_mess(self):
        user = current_user
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute (f"""
            SELECT message, email
            FROM messages , user
            WHERE recipient_id = ? and user.id = sender_id
            
            """,[user.id])
        m = m.fetchall()
        conn.commit()
        cursor.execute('''DELETE FROM messages 
                          WHERE recipient_id=?''', [user.id])
        return m 


