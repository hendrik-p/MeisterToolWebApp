from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, FloatField, RadioField

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

    attribute_default = 13
    skill_default = 0
    mod_defaut = 0
    attribute1 = IntegerField('Eigenschaft 1')
    attribute2 = IntegerField('Eigenschaft 2')
    attribute3 = IntegerField('Eigenschaft 3')
    skill = IntegerField('Talentwert')
    mod = IntegerField('Modifikator')
    roll_button = SubmitField('Würfeln')

travel_conditions_choices = [('perfect', 'Perfekt'),
                             ('good', 'Gut'),
                             ('average', 'Durchschnittlich'),
                             ('bad', 'Schlecht')]

computation_methods_choices = [('simple', 'Einfache Berechnung'),
                               ('simulation', 'Simulation')]

class TravelForm(FlaskForm):

    group_size_default = 1
    dist_default = 10
    travel_conditions_default = 'good'
    computation_methods_default = 'simple'
    group_size = IntegerField('Gruppengröße')
    dist_foot = FloatField('Zu Fuß')
    dist_boat = FloatField('Flusskahn')
    dist_carriage = FloatField('Reisekutsche')
    dist_sea_hammock = FloatField('Seereise, Hängematte')
    dist_sea_cabin = FloatField('Seereise, Kabine')
    dist_horse = FloatField('Pferd')
    travel_conditions = SelectField('Reisebedingungen', choices=travel_conditions_choices)
    computation_methods = RadioField('Berechnungsmethode', choices=computation_methods_choices)
    submit_field = SubmitField('Berechne')

