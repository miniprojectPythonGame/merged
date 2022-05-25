import pygame
import sys
from pygame.locals import *

from src.components.Button import Button
from src.components.Label import Label
from src.components.ListElement import ListElement
from src.components.ScrollableList import ScrollableList
from src.components.Plane import Plane

from .fight.Fight import Fight
from .Measurements import Measurements as meas
from src.globals.const_values import getDifficulty


def Tavern(screen, mainClock, user):

    def reloadPreview(activeQuest):
        p_background = Plane(meas.p_background['x'], meas.p_background['y'],
                             meas.p_background['width'], meas.p_background['height'],
                             meas.p_background['color'], screen)

        lb_quest_title = Label(activeQuest.name, meas.lb_quest_title['font'], meas.lb_quest_title['color'],
                               screen, meas.lb_quest_title['x'], meas.lb_quest_title['y'])

        lb_difficulty_header = Label("Difficulty: ", meas.lb_difficulty_header['font'],
                                     meas.lb_difficulty_header['color'], screen,
                                     meas.lb_difficulty_header['x'], meas.lb_difficulty_header['y'])

        lb_min_level_header = Label("Min level: ", meas.lb_min_level_header['font'],
                                     meas.lb_min_level_header['color'], screen,
                                     meas.lb_min_level_header['x'], meas.lb_min_level_header['y'])

        bt_fight = Button(meas.bt_fight['color'], meas.bt_fight['x'], meas.bt_fight['y'],
                          meas.bt_fight['width'], meas.bt_fight['height'], screen,
                          meas.bt_fight['text'], meas.header_tertiary_font,
                          border_radius=meas.bt_fight['border-radius'])

        return p_background, lb_quest_title, bt_fight, lb_difficulty_header, lb_min_level_header

    showHand = False
    running = True
    hero = user.currentHero
    activeQuest = None

    quest_list = user.currentHero.quests.quest_list

    label_page = Label(meas.label_page['text'], meas.label_page['font'], meas.label_page['color'], screen,
                       meas.label_page['x'], meas.label_page['y'], meas.label_page['anchor'])
    bt_return = Button(meas.bt_return['color'], meas.bt_return['x'], meas.bt_return['y'],
                       meas.bt_return['width'], meas.bt_return['height'], screen,
                       path=meas.bt_return['path'])
    list_elements = []
    for quest in quest_list:
        difficulty = getDifficulty(quest.difficulty)
        list_elements.append(ListElement(meas.le_general['x'],
                                         meas.le_general[
                                             'y'] + 0 * meas.list_element_padding + 0 * meas.list_element_height,
                                         meas.le_general['width'], meas.le_general['height'],
                                         meas.le_general['colors'], screen, quest.name, difficulty,
                                         "", "",
                                         object=quest))

    sl_quests = ScrollableList(meas.sl_quests['x'], meas.sl_quests['y'], screen, list_elements,
                               meas.list_element_height, meas.list_element_padding)

    p_background = None
    lb_quest_title = None
    ml_quest_description = None
    lb_min_level_header = None
    lb_min_leevl_value = None
    lb_difficulty_header = None
    lb_difficulty_value = None
    lb_gold_header = None
    lb_gold_value = None
    lb_teasure_header = None
    bt_fight = None

    displayedContent = [
        label_page, bt_return,
    ]

    while running:
        screen.fill((255, 255, 255))
        if showHand:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for elem in displayedContent:
            elem.draw()

        sl_quests.draw()

        if activeQuest is not None:
            p_background.draw()
            lb_quest_title.draw()
            bt_fight.draw()
            lb_difficulty_header.draw()
            lb_min_level_header.draw()

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # LEFT CLICK
                if event.button == 1:
                    # HANDLE RETURN BUTTON
                    if bt_return.rect.collidepoint(event.pos):
                        running = False
                        break

                    if activeQuest is not None and bt_fight.rect.collidepoint(event.pos):
                        Fight(screen, mainClock, hero, activeQuest.enemy)
                        break

                    for questLine in sl_quests.list:
                        if questLine.rect.collidepoint(event.pos):
                            activeQuest = questLine.object
                            print(activeQuest)
                            p_background, lb_quest_title, bt_fight, lb_difficulty_header, lb_min_level_header = reloadPreview(activeQuest)
                            break
                # SCROLL
                if event.button == 4:
                    sl_quests.onScrollUp()
                    break

                elif event.button == 5:
                    sl_quests.onScrollDown()
                    break

        pygame.display.update()
        mainClock.tick(60)