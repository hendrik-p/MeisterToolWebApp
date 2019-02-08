import sqlite3
from flask import Flask, render_template, g
from flask_wtf import FlaskForm
from wtforms import SelectField

app = Flask(__name__)
app.secret_key = 'my_secret_development_key'

regions = ['Mittelreich',
           'Orkland',
           'Thorwal',
           'Nostria',
           'Andergast',
           'Horasreich',
           'Zyklopeninseln',
           'Alanfa',
           'Dschungel des Südens',
           'Südmeer',
           'Kalifat',
           'Länder der Tulamiden',
           'Aranien',
           'Maraskan',
           'Schattenlande',
           'Salamandersteine',
           'Svelltal',
           'Bornland',
           'Hoher Norden',
           'Mhanadistan',
           'Wüste Khom']

select_region_choices = []
query_names = {}
for region in regions:
    value = region.lower().replace(' ', '_')
    value = value.replace('ä', 'ae')
    value = value.replace('ö', 'oe')
    value = value.replace('ü', 'ue')
    select_region_choices.append((value, region))
    query_names[value] = region

db_path = 'odatastools.db'

def get_database():
    db = getattr(g, '_database', None)
    if not db:
        g._database = sqlite3.connect(db_path)
        db = g._database
    return db

class DangersForm(FlaskForm):

    region = SelectField('Region', choices=select_region_choices)


@app.route('/', methods=['GET', 'POST'])
def dangers():
    form = DangersForm()
    region = form.region.data
    animal_query = 'select Name, Quelle from animals where[%s]=1 order by name' % query_names[region]
    monster_query = 'select Name, Quelle from ungeheuer where[%s]=1 order by name' % query_names[region]
    db_conn = get_database()
    db_cursor = db_conn.cursor()
    db_cursor.execute(animal_query)
    animal_rows = db_cursor.fetchall()
    db_cursor.execute(monster_query)
    monster_rows = db_cursor.fetchall()
    return render_template('index.html', form=form, animal_rows=animal_rows,
                           monster_rows=monster_rows)

if __name__ == '__main__':
    app.run()

