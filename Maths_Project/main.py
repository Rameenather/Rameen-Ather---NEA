from flask import Flask
from __init__ import create_app
import sqlite3
from student import student
from database_attempt import *


#creating the app :P
app = create_app()


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






if __name__ == '__main__':
    app.run(debug=True)


