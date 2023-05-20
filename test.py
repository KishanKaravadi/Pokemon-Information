import pokebase as pb
from pokebase import cache
from pokebase.common import ENDPOINTS

cache.set_cache('testing')

hi = pb.api.get_data('berry', 1, force_lookup=True)
print(hi)
