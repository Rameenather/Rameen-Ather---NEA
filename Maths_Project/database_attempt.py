from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import db
import json
from models import User
import random
import sqlite3
from datetime import date , datetime
import smtplib


def getforms():
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
        


def get_questions(topic):
    """Gets the question of the topic the user wants"""

    import base64
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    m = cursor.execute (f"""
        SELECT question, id, answer
        FROM questions
        WHERE topic = ?
        """,[topic])
    print(m)

    for x in m:
        rec_data = x[0]

    with open('static/q1.png','wb') as f:
        f.write(rec_data)
    

    conn.commit()
    cursor.close()
    conn.close()
    

def get_topic():
    if request.method == 'POST':
        topic = request.form.get('sclt2')
        if topic == None:
            pass
        else:
            get_questions(topic)
        print(topic)





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



