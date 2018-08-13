

def heal(entity, amount_of_hp):
    if entity.life + amount_of_hp > entity.max_life:
        entity.life = entity.max_life
    else: 
        entity.life += amount_of_hp


def energyup(entity, par):
    if entity.mana + par > entity.max_mana:
        entity.mana = entity.max_mana
    else: 
        entity.mana += par
