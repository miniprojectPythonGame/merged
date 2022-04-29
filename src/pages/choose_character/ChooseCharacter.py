import pygame
import sys
from pygame.locals import *

from src.components.Label import Label
from src.components.Button import Button

from src.components.CharacterSlider import CharacterSlider
from .Measurements import Measurements as meas
from src.globals.mock_data import createNew as createNew

from src.pages.create_character.CreateCharacter import CreateCharacter
from src.pages.city_map.CityMap import CityMap


def ChooseCharacter(screen, mainClock, user):
    print(user.Heroes)

    for key in user.Heroes.keys():
        print(user.Heroes[key].heroClass)

    running = True

    label_page = Label(meas.label_page['text'], meas.label_page['font'], meas.label_page['color'], screen,
                       meas.label_page['x'], meas.label_page['y'], meas.label_page['anchor'])

    characters = [{
        "key": key,
        "name": user.Heroes[key].name,
        "spec": str(user.Heroes[key].heroClass),
        "level": user.Heroes[key].lvl,
        "img": '../images/characters/' + str(user.Heroes[key].heroClass).lower() + '_' + str(user.Heroes[key].avatar_id) + '_rect.jpg',
    } for key in user.Heroes.keys()]

    curr_index = 1
    curr_key = characters[curr_index]['key']

    cs_characters = CharacterSlider(characters + [createNew], screen)

    bt_prev = Button(meas.bt_prev['color'], meas.bt_prev['x'], meas.bt_prev['y'],
                     meas.bt_prev['width'], meas.bt_prev['height'], screen,
                     meas.bt_prev['text'], meas.bt_prev['font'], path=meas.bt_prev['path'])

    bt_next = Button(meas.bt_next['color'], meas.bt_next['x'], meas.bt_next['y'],
                     meas.bt_next['width'], meas.bt_next['height'], screen,
                     meas.bt_next['text'], meas.bt_next['font'], path=meas.bt_next['path'])

    bt_delete = Button(meas.bt_delete['color'], meas.bt_delete['x'], meas.bt_delete['y'],
                       meas.bt_delete['width'], meas.bt_delete['height'], screen,
                       meas.bt_delete['text'], meas.input_font)

    while running:
        screen.fill((255, 255, 255))

        label_page.draw()
        cs_characters.draw()

        bt_prev.draw()
        bt_next.draw()
        if cs_characters.curr_main.class_name != '':
            bt_delete.draw()

        mx, my = pygame.mouse.get_pos()

        # HOVERS
        # Button login: hover
        if cs_characters.curr_main.rect.collidepoint((mx, my)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Button login hover
        if bt_delete.rect.collidepoint((mx, my)):
            bt_delete.onHoverOn()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            bt_delete.onHoverOff()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                # 'Previous' button
                if bt_prev.rect.collidepoint(event.pos):
                    if cs_characters.curr_main.class_name != '' and 0 < curr_index:
                        curr_index -= 1
                        curr_key = characters[curr_index]['key']
                    cs_characters.swipeLeft()

                # 'Next' button
                if bt_next.rect.collidepoint(event.pos):
                    cs_characters.swipeRight()
                    if curr_index + 1 < len(characters):
                        curr_index += 1
                        curr_key = characters[curr_index]['key']

                if bt_delete.rect.collidepoint(event.pos):
                    user.removeHero(curr_key)
                    characters = [{
                        "key": key,
                        "name": user.Heroes[key].name,
                        "spec": str(user.Heroes[key].heroClass),
                        "level": user.Heroes[key].lvl,
                        "img": '../images/characters/' + str(user.Heroes[key].heroClass).lower() + '_' + str(
                            user.Heroes[key].avatar_id) + '_rect.jpg',
                    } for key in user.Heroes.keys()]

                    cs_characters = CharacterSlider(characters + [createNew], screen)
                    curr_index = 1
                    curr_key = characters[curr_index]['key']

                if cs_characters.curr_main.rect.collidepoint(event.pos):
                    if cs_characters.curr_main.class_name == '':
                        CreateCharacter(screen, mainClock, user)
                        user.getHeroes()

                        characters = [{
                            "key": key,
                            "name": user.Heroes[key].name,
                            "spec": str(user.Heroes[key].heroClass),
                            "level": user.Heroes[key].lvl,
                            "img": '../images/characters/' + str(user.Heroes[key].heroClass).lower() + '_' + str(
                                user.Heroes[key].avatar_id) + '_rect.jpg',
                        } for key in user.Heroes.keys()]

                        cs_characters = CharacterSlider(characters + [createNew], screen)
                        curr_index = 1
                        curr_key = characters[curr_index]['key']
                    else:
                        user.chooseHero(characters[curr_index]['key'])
                        # if swap -> true, so it goes on
                        # if logout -> false, so will stop
                        running = CityMap(screen, mainClock, user)
                        print("Logout: ChooseCharacter.py -> LoginPage.py")

        pygame.display.update()
        mainClock.tick(60)
