
import pokebase as pb

from pokebase import cache
from pokebase import interface
import pyautogui
import pytesseract
import re
import numpy as np
from PIL import Image, ImageFilter
import pygetwindow as gw

cache.set_cache('testing')


def get_info(poke_name) -> dict:
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


TOP_LEFT = (2251, 85)
BOTTOM_RIGHT = (2460, 119)

male = [11, 68, 240]
female = [238, 15, 7]

hi = gw.getWindowsWithTitle("Ryujinx ")[0]
print(hi)
left = hi.left+(hi.width*(983/1296))
top = hi.top+(hi.height*(78/804))
width = 209
height = 34*(hi.height/804)


def get_name_from_top() -> str:
    pokemon_image = pyautogui.screenshot(
        region=(left, top, width, height))
    pokemon_image.save('hi.png')
    processed_image = keep_colors_close_to_black(pokemon_image)
    processed_image.save('bye.png')
    pokemon_name = pytesseract.image_to_string(processed_image)
    true_pokemon_name = re.sub(r"[^a-zA-Z0-9 -]", "", pokemon_name)
    return true_pokemon_name


def keep_colors_close_to_black(image, threshold=71) -> Image:
    # Load the image using PIL
    # Convert the image to grayscale
    grayscale_image = image.convert("L")

    # Apply threshold to filter out non-black colors
    filtered_image = grayscale_image.point(lambda p: p < threshold and 255)

    # Convert the filtered image back to RGB
    filtered_image_rgb = filtered_image.convert("RGB")

    inverted_image = Image.eval(filtered_image_rgb, lambda p: 255 - p)

    dilated_image = inverted_image.filter(
        ImageFilter.MinFilter(1))
    # Display or save the filtered image
    dilated_image.save('dilate.png')
    return dilated_image


hi = get_name_from_top()
print(hi)
