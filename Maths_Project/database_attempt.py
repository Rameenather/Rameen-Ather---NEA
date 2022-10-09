from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from __init__ import db
import json
from models import User
import random


def getforms():
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
        















