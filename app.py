import sqlite3
from flask import Flask, render_template, g, request
from forms import DangersForm, DiceRollForm
from functions import fetch_animals_and_monsters, dice_roll

app = Flask(__name__)
app.secret_key = 'my_secret_development_key'

db_path = 'odatastools.db'

def get_database():
    db = getattr(g, '_database', None)
    if not db:
        g._database = sqlite3.connect(db_path)
        db = g._database
    return db

@app.route('/')
def index():
    return render_template('index.html')

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
        form.attribute1.data = default_value
        form.attribute2.data = default_value
        form.attribute3.data = default_value
        form.skill.data = 0
        form.mod.data = 0
    if form.validate_on_submit():
        att1 = form.attribute1.data
        att2 = form.attribute2.data
        att3 = form.attribute3.data
        skill = form.skill.data
        mod = form.mod.data
        rolls, result_str = dice_roll(att1, att2, att3, skill, mod)
        return render_template('dice.html', form=form, rolls=rolls,
                               result_str=result_str)
    print('did not validate')
    return render_template('dice.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

