import random

def fetch_animals_and_monsters(db_conn, region):
    animal_query = 'select Name, Quelle from animals where[%s]=1 order by name' % region
    monster_query = 'select Name, Quelle from ungeheuer where[%s]=1 order by name' % region
    db_cursor = db_conn.cursor()
    db_cursor.execute(animal_query)
    animal_rows = db_cursor.fetchall()
    db_cursor.execute(monster_query)
    monster_rows = db_cursor.fetchall()
    return animal_rows, monster_rows

def remaining_skillpoints_to_qs(remaining):
    if remaining < 0:
        return 0
    if remaining < 4:
        return 1
    if remaining < 7:
        return 2
    if remaining < 10:
        return 3
    if remaining < 13:
        return 4
    if remaining < 16:
        return 5
    return 6

def dice_roll(att1, att2, att3, skill, mod):
    att1 += mod
    att2 += mod
    att3 += mod
    roll1 = random.randint(1, 20)
    roll2 = random.randint(1, 20)
    roll3 = random.randint(1, 20)
    remaining = skill
    if roll1 > att1:
        diff = roll1 - att1
        remaining -= diff
    if roll2 > att2:
        diff = roll2 - att2
        remaining -= diff
    if roll3 > att3:
        diff = roll3 - att3
        remaining -= diff
    qs = remaining_skillpoints_to_qs(remaining)
    result_str = 'Misserfolg' if qs == 0 else 'Erfolg mit QS %d' % qs
    rolls = (roll1, roll2, roll3)
    if len([r for r in rolls if r == 1]) > 1:
        result_str = 'Kritischer Erfolg'
    if len([r for r in rolls if r == 20]) > 1:
        result_str = 'Patzer'
    return rolls, result_str

