from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send
from __init__ import create_app, create_database
import sqlite3
from account import account
from database_attempt import *
from os import path



#creating the app :P
app = create_app()

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    # Save the user's connection in the list of connected users
    connected_users[request.sid] = request.namespace

@socketio.on('disconnect')
def handle_disconnect():
    # Remove the user's connection from the list of connected users
    del connected_users[request.sid]


conn = sqlite3.connect('database.db')
#conn = sqlite3.connect('image.db')
cursor = conn.cursor()

#Creating the questions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    topic TEXT NOT NULL,
    question BLOP NOT NULL,
    answer BLOP NOT NULL,
    marks INTEGER NOT NULL)""")

#Create the "users" and "messages" tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages
    (sender_id INTEGER NOT NULL, 
    recipient_id INTEGER NOT NULL, 
    message text NOT NULL)""")


#storing the marks the user got after completing questions
cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_marks (question_done_id INTEGER PRIMARY KEY NOT NULL,
    date_entered DATE NOT NULL,
    acc_id INTEGER NOT NULL,
    qa_id INTEGER NOT NULL,
    marks INTEGER ,
    FOREIGN KEY(acc_id)
        REFERENCES user (id),
    FOREIGN KEY (qa_id)
        REFERENCES questions (id))""")

 #temporarily storing the question
cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_answer (question_done_id INTEGER NOT NULL,
    user_answers BLOP,
    FOREIGN KEY(question_done_id)
        REFERENCES account_marks (question_done_id))""")




#creating one of the tables for storing logs
cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic1 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    lipid INTEGER NOT NULL,
    carbohydrates INTEGER NOT NULL,
    protein_and_enzymes INTEGER NOT NULL,
    DNA INTEGER NOT NULL,
    ATP INTEGER NOT NULL,
    Water_and_inorganic_ions INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic2 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    cell_structure INTEGER NOT NULL,
    transport_across_membrane INTEGER NOT NULL,
    cell_cycle INTEGER NOT NULL,
    immune_system INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic3 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    gas_exchange INTEGER NOT NULL,
    digestion_and_absorption INTEGER NOT NULL,
    mass_transport INTEGER NOT NULL, 
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic4 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    protein_synthesis INTEGER NOT NULL,
    biodiversity INTEGER NOT NULL,
    genetic_diversity INTEGER NOT NULL, 
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic5 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    photosynthesis INTEGER NOT NULL,
    respiration INTEGER NOT NULL,
    nitrogen_cycle INTEGER NOT NULL,
    energy_and_ecosystem INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic6 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    response_to_stimuli INTEGER NOT NULL,
    nervous_coordination_and_muscles INTEGER NOT NULL,
    homeostasis INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic7 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    inherited_change INTEGER NOT NULL,
    population_and_evolution INTEGER NOT NULL,
    population_in_ecosystems INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic8 (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    gene_expression INTEGER NOT NULL,
    recombinant_DNA_technology INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pure (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    proof INTEGER NOT NULL,
    algebra_and_functions INTEGER NOT NULL,
    coordinate_geometry INTEGER NOT NULL,
    sequences_and_series INTEGER NOT NULL,
    trigonometry INTEGER NOT NULL,
    exponentials_and_logarithms INTEGER NOT NULL,
    differentiation INTEGER NOT NULL,
    integration INTEGER NOT NULL,
    numerical_methods INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)


cursor.execute("""
    CREATE TABLE IF NOT EXISTS mech (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    vectors INTEGER NOT NULL,
    quantities_and_units_in_mechanics INTEGER NOT NULL,
    kinematics INTEGER NOT NULL,
    forces_and_Newton’s_laws INTEGER NOT NULL,
    moments INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stats (account_id INTEGER NOT NULL,
    date_entered DATE PRIMARY KEY NOT NULL,
    statistical_sampling INTEGER NOT NULL,
    data_presentation_and_interpretation INTEGER NOT NULL,
    probability INTEGER NOT NULL,
    statistical_distributions INTEGER NOT NULL,
    statistical_hypothesis_testing INTEGER NOT NULL,
    FOREIGN KEY(account_id)
        REFERENCES user (id))
    """)


tables_biology = {
         '1': ['Lipids', 'Carbohydrates','Proteins and Enzymes','DNA ', 'ATP', 'Water and Inorgranic ions'],
         '2': ['Cell structure','Transport across cell membranes','Cell cycle','Immune system'],
         '3': ['Gas Exchange','Digestion and Absorption','Mass Transport'],
         '4': ['Protein Synthesis','Biodiversity ','Genetic Diversity '],
         '5': ['Photosynthesis','Respiration','Nitrogen Cycle','Energy and ecosystem'],
         '6': ['Homeostasis','Nervous coordination and muscles','Response to stimuli',],
         '7': ['Populations in ecosystems','Inheritance and genetic crosses','Evolution and Speciation'],
         '8': ['Gene Mutation','Stem cells','Genetic Fingerprinting ','Gene Expression and Cancer']
          }

#put 6 questions for now, so i can code the stuff that the questions are needed for.
#topic = "lipid"
#mark = 8

#with open('questions/biology/lipid-1.PNG' , 'rb') as f:
 #   question = f.read()

#with open('questions/biology/lipid-1-ans.PNG','rb') as a:
 #   ans = a.read()

#cursor.execute("""INSERT INTO questions (topic, question, answer, marks) VALUES (?,?,?,?)""",(topic,question,ans,mark))

send_email()



conn.commit()
cursor.close()
conn.close()




#---------------------------------------------------------------------------------------#

connected_user = {}
import sys




if __name__ == '__main__':
    app.run(debug=True)
    
    
