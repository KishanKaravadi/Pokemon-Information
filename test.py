import pokebase as pb
from pokebase import cache
from pokebase.common import ENDPOINTS

# cache.set_cache('testing')

hi = pb.api.get_data('type', force_lookup=True)
for key in hi['results']:
    print(key)
