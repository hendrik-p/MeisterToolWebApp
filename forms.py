from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField

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

class DangersForm(FlaskForm):

    select_region_choices = []
    query_names = {}
    for region in regions:
        value = region.lower().replace(' ', '_')
        value = value.replace('ä', 'ae')
        value = value.replace('ö', 'oe')
        value = value.replace('ü', 'ue')
        select_region_choices.append((value, region))
        query_names[value] = region

    region = SelectField('mittelreich', choices=select_region_choices)


class DiceRollForm(FlaskForm):

    attribute1 = IntegerField('attribute1')
    attribute2 = IntegerField('attribute2')
    attribute3 = IntegerField('attribute3')
    skill = IntegerField('skill')
    mod = IntegerField('mod')
    roll_button = SubmitField('Würfeln')


