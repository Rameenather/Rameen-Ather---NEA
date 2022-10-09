from flask import Flask
from __init__ import create_app
import sqlite3




app = create_app()



conn = sqlite3.connect('image.db')
cursor = conn.cursor()



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

tables_maths = {
    '1':[],
    '2':[],
    '3':[],
    '4':[]
    
    }




conn.commit()
cursor.close()
conn.close()




#---------------------------------------------------------------------------------------#








if __name__ == '__main__':
    app.run(debug=True)


