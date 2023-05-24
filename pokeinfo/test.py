
import pokebase as pb

from pokebase import cache
from pokebase import interface

cache.set_cache('testing')


def getInfo(poke_name) -> dict:
    poke_id = interface._convert_name_to_id('pokemon', poke_name)
    poke_type = {'bug': 1, 'dark': 1, 'dragon': 1, 'electric': 1, 'fairy': 1, 'fighting': 1, 'fire': 1, 'flying': 1,
                 'ghost': 1, 'grass': 1, 'ground': 1, 'ice': 1, 'normal': 1, 'poison': 1, 'psychic': 1, 'rock': 1, 'steel': 1, 'water': 1}
    poke = pb.api.get_data(
        'pokemon', resource_id=poke_id, force_lookup=True)
    for type in poke['types']:
        name = type['type']['name']
        type_id = interface._convert_name_to_id('type', name)
        types = pb.api.get_data('type', resource_id=type_id, force_lookup=True)
        for category in ['double_damage_from']:
            for obj in types['damage_relations'][category]:
                poke_type[obj['name']] *= 2
        for category in ['half_damage_from']:
            for obj in types['damage_relations'][category]:
                poke_type[obj['name']] *= 1/2
        for category in ['no_damage_from']:
            for obj in types['damage_relations'][category]:
                poke_type[obj['name']] *= 0
    return poke_type


print(getInfo('alola-diglett'))
