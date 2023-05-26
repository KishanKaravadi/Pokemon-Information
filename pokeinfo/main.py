import PySimpleGUI as sg
import pokebase as pb
from pokebase import interface
import pytesseract
import pyautogui
import re
import numpy as np
from PIL import Image, ImageFilter
import pygetwindow as gw

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

"""
    Demo - A simple minimal window with a material design feel
    
    Contains base64 images for:
    * The PSG Yellow Graphic
    * The 2 toggle buttons
    * The large spinning animation

    Copyright 2021 PySimpleGUI
"""


def get_name_from_top(loc) -> str:

    pokemon_image = pyautogui.screenshot(
        region=loc)
    processed_image = keep_colors_close_to_black(pokemon_image)
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


def get_info(poke_name) -> dict or None:
    poke_id = interface._convert_name_to_id('pokemon', poke_name)
    if poke_id == None:
        return None
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


def getTypes(poke_name):
    pokemon_types = []
    poke_id = interface._convert_name_to_id('pokemon', poke_name)
    if poke_id == None:
        return None
    poke = pb.api.get_data(
        'pokemon', resource_id=poke_id, force_lookup=True)
    for type in poke['types']:
        pokemon_types.append(type['type']['name'])
    return pokemon_types


def main(poke_name):
    sg.theme('light grey')
    BLUE_BUTTON_COLOR = '#FFFFFF on #2196f2'
    GREEN_BUTTON_COLOR = '#FFFFFF on #00c851'
    LIGHT_GRAY_BUTTON_COLOR = f'#212021 on #e0e0e0'
    DARK_GRAY_BUTTON_COLOR = '#e0e0e0 on #212021'

    POKEMON_TYPE_FROM = get_info(poke_name)
    if POKEMON_TYPE_FROM == None:
        poke_name = 'charmander'
        POKEMON_TYPE_FROM = get_info(poke_name)

    POKEMON_TYPE_SORTED = dict(
        sorted(POKEMON_TYPE_FROM.items(), key=lambda x: -x[1]))

    SUPER_EFFECTIVE = [key for key,
                       value in POKEMON_TYPE_SORTED.items() if value == 2]

    SUPER_SUPER_EFFECTIVE = [key for key,
                             value in POKEMON_TYPE_SORTED.items() if value == 4]

    NEUTRAL = [key for key,
               value in POKEMON_TYPE_SORTED.items() if value == 1]

    NEUTRAL_FIRST_HALF = NEUTRAL[0:len(NEUTRAL)//2]

    NEUTRAL_SECOND_HALF = NEUTRAL[len(NEUTRAL)//2:]

    RESISTANCE = [key for key, value in POKEMON_TYPE_SORTED.items()
                  if value == 0.5]

    EVEN_MORE_RESISTANCE = [key for key, value in POKEMON_TYPE_SORTED.items()
                            if value == 0.25]

    IMMUNITY = [key for key, value in POKEMON_TYPE_SORTED.items()
                if value == 0]

    pokemon_types = getTypes(poke_name)
    if pokemon_types == None:
        getTypes('charmander')

    print(pokemon_types)

    layout = [[sg.Col([[sg.T('Welcome to my App')],
                       [sg.T('Your license status: '), sg.T(
                           'Trial', k='-LIC STATUS-')],
                       [sg.Image(filename='assets/'+poke_type+'.png', subsample=3)
                           for poke_type in pokemon_types],
                       [sg.T()],

                       [sg.Image(data=pb.SpriteResource(
                           'pokemon', interface._convert_name_to_id('pokemon', poke_name)).img_data)],

                       [sg.Image(filename="assets/"+name+".png", subsample=2)
                        for name in SUPER_SUPER_EFFECTIVE] + [sg.Image(filename="assets/"+name+".png", subsample=2)
                                                              for name in SUPER_EFFECTIVE],
                       [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='#73d216', justification='center', font=('Helvetica', 19))
                        for name in SUPER_SUPER_EFFECTIVE] + [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='#4e9a06', justification='center', font=('Helvetica', 19))
                                                              for name in SUPER_EFFECTIVE],

                       [sg.Image(filename="assets/"+name+".png", subsample=2)
                        for name in NEUTRAL_FIRST_HALF],
                       [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='slate grey', justification='center', font=('Helvetica', 19))
                        for name in NEUTRAL_FIRST_HALF],

                       [sg.Image(filename="assets/"+name+".png", subsample=2)
                        for name in NEUTRAL_SECOND_HALF],
                       [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='slate grey', justification='center', font=('Helvetica', 19))
                        for name in NEUTRAL_SECOND_HALF],

                       [sg.Image(filename="assets/"+name+".png", subsample=2)
                        for name in RESISTANCE] + [sg.Image(filename="assets/"+name+".png", subsample=2)
                                                   for name in EVEN_MORE_RESISTANCE],
                       [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='#a40000', justification='center', font=('Helvetica', 19))
                        for name in RESISTANCE] + [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='#7c0000', justification='center', font=('Helvetica', 19))
                                                   for name in EVEN_MORE_RESISTANCE],

                       [sg.Image(filename="assets/"+name+".png", subsample=2)
                        for name in IMMUNITY],
                       [sg.Text(text=POKEMON_TYPE_FROM[name], size=(5, 2), text_color='#ffdd57', background_color='#2e3436', justification='center', font=('Helvetica', 19))
                        for name in IMMUNITY],

                       [sg.B(image_data=T_OFF, k='-TOGGLE1-', metadata=False, button_color=sg.theme_background_color()),
                        sg.B(image_data=T_OFF, k='-TOGGLE2-',
                             button_color=sg.theme_background_color(), metadata=True),
                        sg.B(image_data=T_OFF, k='-TOGGLE3-', metadata=False,
                             button_color=sg.theme_background_color()),
                        sg.B(image_data=T_OFF, k='-TOGGLE4-', button_color=sg.theme_background_color(), metadata=True)],
                       [sg.Text(text='Alolan', font=('Helvetica', 17), justification='center'), sg.Text(text='Paldean', font=('Helvetica', 17), justification='center'), sg.Text(
                           text='Galarian', font=('Helvetica', 17), justification='center'), sg.Text(text='Hisuian', font=('Helvetica', 17), justification='center')],
                       [sg.Input(key='-POKENAME-',
                                 background_color='grey', text_color='black', expand_x=False, font=('Helvetica', 19), focus=True, justification='center', size=(40, 50))],
                       [sg.B('Wild Pokemon', size=(14, 2), button_color=BLUE_BUTTON_COLOR),
                        sg.B('Override', size=(14, 2),
                             button_color=GREEN_BUTTON_COLOR),
                        sg.B('Exit', size=(14, 2), button_color=BLUE_BUTTON_COLOR)],
                       [sg.Image(data=BLANK, k='-GIF-', metadata=0)],
                       [sg.T('The end of "my App"')]], element_justification='c', k='-TOP COL-')]]

    window = sg.Window('PokeInfo', layout=layout,
                       location=(-7, 0))

    while True:             # Event Loop
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event.startswith('-TOGGLE'):
            state = window[event].metadata = not window[event].metadata
            window[event].update(image_data=T_ON if state else T_OFF)
        if event == '-TOGGLE1-':
            window.close()
            if '-' in poke_name:
                poke_name = poke_name.split("-", 1)[0]
            main(poke_name + '-alola')
        elif event == '-TOGGLE2-':
            window.close()
            if '-' in poke_name:
                poke_name = poke_name.split("-", 1)[0]
            main(poke_name + '-paldea')
        elif event == '-TOGGLE3-':
            window.close()
            if '-' in poke_name:
                poke_name = poke_name.split("-", 1)[0]
            main(poke_name + '-galar')
        elif event == '-TOGGLE4-':
            window.close()
            if '-' in poke_name:
                poke_name = poke_name.split("-", 1)[0]
            main(poke_name + '-hisui')
        elif event == 'Wild Pokemon':
            ryujinx = gw.getWindowsWithTitle("Ryujinx ")[0]
            left = ryujinx.left+((ryujinx.width*983)/1296)
            top = ryujinx.top+((ryujinx.height*84)/804)
            width = 209
            height = 34
            window.close()
            wild_pokemon = get_name_from_top((left, top, width, height))
            main(wild_pokemon.lower())
        elif event == 'Exit':
            ryujinx = gw.getWindowsWithTitle("Ryujinx ")[0]
            left = ryujinx.left+((ryujinx.width*983)/1296)
            top = ryujinx.top+((ryujinx.height*84)/804)
            width = 209
            height = 34
            window.close()
            wild_pokemon = get_name_from_top((left, top, width, height))
            main(wild_pokemon.lower())
        elif event == 'Override':
            window.close()
            main(values['-POKENAME-'])

    window.close()


if __name__ == '__main__':
    BLANK = b'iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB7SURBVHhe7cExAQAAAMKg9U9tDQ8gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADtQAkK8AAT0JXwIAAAAASUVORK5CYII='
    T_OFF = b'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'
    T_ON = b'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'

    main('charmander')
