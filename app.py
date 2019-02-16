import os
import sqlite3

from flask import Flask, render_template, g, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

from forms import DangersForm, DiceRollForm, TravelForm
from functions import fetch_animals_and_monsters, dice_roll
import odatasfunctions as of

app = Flask(__name__)
bootstrap = Bootstrap(app)
nav = Nav()
nav.init_app(app)

app.secret_key = 'my_secret_development_key'

db_path = '%s/odatastools.db' % os.path.dirname(os.path.realpath(__file__))

@nav.navigation()
def get_navbar():
    return Navbar('DSA5 MeisterTools',
                  View('Home', 'index'),
                  View('Reisehelfer','travel'),
                  View('Wildtiere und Ungeheuer', 'dangers'),
                  View('Würfeln', 'dice'))

def get_database():
    db = getattr(g, '_database', None)
    if not db:
        g._database = sqlite3.connect(db_path)
        db = g._database
    return db

@app.route('/')
def index():
    return render_template('index.html')

class TravelComputationResult(object):

    def __init__(self, travel_days, trans_cost, trans_method_cost, food, water):
        self.travel_days = int(travel_days)
        self.transport_cost = of.Geldrechner(trans_cost, 'Heller')
        self.food_cost = of.Geldrechner(food, 'Heller')
        self.total_cost = of.Geldrechner(trans_cost + food, 'Heller')
        qs_multipliers = [1.3, 1, 0.95, 0.92, 0.9, 0.89, 0.87, 0.8]
        row_labels = ['Fehlschlag', 'QS 1', 'QS 2', 'QS 3', 'QS 4', 'QS 5', 'QS 6']
        self.haggling_table = []
        for label, qs_multiplier in zip(row_labels, qs_multipliers):
            col = [label]
            for cost in [food] + list(trans_method_cost):
                c = of.GeldrechnerKurz(qs_multiplier * cost, 'Heller')
                col.append(c)
            self.haggling_table.append(col)

@app.route('/travel', methods=['GET', 'POST'])
def travel():
    form = TravelForm()
    if request.method == 'GET':
        form.group_size.data = form.group_size_default
        form.dist_foot.data = form.dist_default
        form.dist_boat.data = form.dist_default
        form.dist_carriage.data = form.dist_default
        form.dist_sea_hammock.data = form.dist_default
        form.dist_sea_cabin.data = form.dist_default
        form.dist_horse.data = form.dist_default
        form.travel_conditions.data = form.travel_conditions_default
        form.computation_methods.data = form.computation_methods_default
    travel_cost_result = None
    if form.validate_on_submit():
        group_size = form.group_size.data
        dist_foot = form.dist_foot.data
        dist_boat = form.dist_boat.data
        dist_carriage = form.dist_carriage.data
        dist_sea_hammock = form.dist_sea_hammock.data
        dist_sea_cabin = form.dist_sea_cabin.data
        dist_horse = form.dist_horse.data
        travel_conditions = form.travel_conditions.data
        computation_methods = form.computation_methods.data
        simulation = computation_methods == 'simulation'
        distances = (dist_horse, dist_foot, dist_boat, dist_carriage,
                     dist_sea_hammock, dist_sea_cabin)
        travel_days, trans_cost, trans_method_cost = of.reisedauerrechnung(distances,
                                                                           group_size,
                                                                           travel_conditions,
                                                                           simulation)
        food, water = of.berechne_nahrungsbedarf(travel_days, group_size,
                                                 travel_conditions, simulation)
        travel_cost_result = TravelComputationResult(travel_days, trans_cost, trans_method_cost, food, water)
    return render_template('travel.html', form=form, travel_cost_result=travel_cost_result)

@app.route('/dangers', methods=['GET', 'POST'])
def dangers():
    form = DangersForm()
    region = form.select_region_choices[0][0]
    if form.validate_on_submit():
        region = form.region.data
    db_conn = get_database()
    animal_rows, monster_rows = fetch_animals_and_monsters(db_conn,
                                                           form.query_names[region])
    return render_template('dangers.html', form=form, animal_rows=animal_rows,
                           monster_rows=monster_rows)

@app.route('/dice', methods=['GET', 'POST'])
def dice():
    default_value = 13
    form = DiceRollForm()
    if request.method == 'GET':
        form.attribute1.data = form.attribute_default
        form.attribute2.data = form.attribute_default
        form.attribute3.data = form.attribute_default
        form.skill.data = form.skill_default
        form.mod.data = form.mod_defaut
    if form.validate_on_submit():
        att1 = form.attribute1.data
        att2 = form.attribute2.data
        att3 = form.attribute3.data
        skill = form.skill.data
        mod = form.mod.data
        rolls, result_str = dice_roll(att1, att2, att3, skill, mod)
        return render_template('dice.html', form=form, rolls=rolls,
                               result_str=result_str)
    return render_template('dice.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

