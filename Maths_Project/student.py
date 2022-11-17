import sqlite3
import database_attempt
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import db
import json
from models import User



class student:
    #student account
    def test(self):
        print("hello test :P")

    def questions(self,topic):
        """Selects questions with the topic wanted (might change)"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        m = cursor.execute ("""
        SELECT question, 
        FROM questions,
        WHERE topic = topic
        """)
        

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

    def enter_answers():
        pass

    def send_answer_to_mark():
        pass

    def mark_received():
        pass

    def send_email():
        pass

    def help():
        pass

    def store_logs_database():
        """Stores the logs entered to the database"""
        if request.method == 'POST':
            lipids = request.form.get('lipids')
            protein = request.form.get('protein')
            water = request.form.get('water')
            atp = request.form.get('atp')
            Carbohydrates = request.form.get('Carbohydrates')
            dna = request.form.get('dna')
            Cellstructure = request.form.get('Cellstructure')
            transportacrossmembrane = request.form.get('transportacrossmembrane')
            cellcycle = request.form.get('cellcycle')
            immunesystem = request.form.get('immunesystem')

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

            }
        print(topic)



    def get_best_topic(self,logs):
       """Calculating the best topic to study at the time might vhange """
       temp = 0
       optimal = None
       temp_list = []
       for i in range(5):
           for j in range(len(self.logs[i+1])):
               temp+=self.logs[i+1][j]
               temp_list.append(temp/4)
               temp = 0
       optimal = higher(temp_list)
       print(optimal)


    def highest(hi):

        highest = 0
        index = 0
        for i in range(1,len(hi)):
            if hi[i] > hi[i-1]:
                highest = hi[i]
                index = i
                print(highest)
        else:
           highest = hi[i-1]
           index = i-1
        return index

    def get_subject_quiz(self):
       pass


class teacher():
    #Teacher account

    def teach(self):
        pass

    def log_teaching():
        pass

    def quick_fire_five():
        pass

    def questions():
        pass

    def mark_scheme():
        pass
    
    def enter_answers():
        pass

    def send_answer_to_mark():
        pass

    def mark_recieved():
        pass 

    def add_points():
        pass

class examiner():
    #examiner account

    def mark():
        pass