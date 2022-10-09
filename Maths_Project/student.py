import sqlite3
import database_attempt


class account:
    def __init__(self,id):
        self.id = id
        
class student(account):
    #student account
    def __init__(self,id):        
        account.__init__(self,id)
        self.id = id
        self.logs = {}

    def questions(self):
        pass

    def report(self):
        pass
    
    def enter_answer_images():
       pass

    def send_email():
        pass


    def calculate_topic(self,logs):
       """Calculating the best topic to study at the time """
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


class teacher(account):
    #Teacher account
    def __init__(self,id,teacher_logs):
        account.__init__(self,id)
        self.tlogs = teacher_logs



    def teach(self):
        pass

class examiner(account):
    #examiner account
    def __init__(self,id):
        account.__init__(self,id)