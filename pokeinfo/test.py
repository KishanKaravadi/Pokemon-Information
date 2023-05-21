import pokebase as pb
from pokeinfo import functions
from importlib import reload
reload(functions)

# cache.set_cache('testing')
# for i in range(1, 19):
#     hi = pb.api.get_data('type', resource_id=i, force_lookup=True)
#     print(hi['damage_relations'])

# hi = functions.get_data_url('type', resource_id=1, force_lookup=True)
# print(hi['damage_relations']['double_damage_from'])
# print(hi['damage_relations']['double_damage_from'])

charm = functions.get_hi()
print(charm, 'hi')
