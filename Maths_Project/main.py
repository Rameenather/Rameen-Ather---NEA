from flask import Flask
from __init__ import create_app
import sqlite3
from student import student

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

#put 6 questions for now, so i can code the stuff that the questions are needed for.
#topic = "lipid"
#mark = 8

#with open('questions/biology/lipid-1.PNG' , 'rb') as f:
 #   question = f.read()

#with open('questions/biology/lipid-1-ans.PNG','rb') as a:
 #   ans = a.read()

#cursor.execute("""INSERT INTO questions (topic, question, answer, marks) VALUES (?,?,?,?)""",(topic,question,ans,mark))









conn.commit()
cursor.close()
conn.close()




#---------------------------------------------------------------------------------------#






if __name__ == '__main__':
    app.run(debug=True)


