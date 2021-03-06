from math import floor
from random import randint
from typing import List, Tuple

from api.game_classes.creatures.bot import Bot
from api.web.WebService import connect_to_db, disconnect_from_db


class Battle(object):
    @classmethod
    def hero_vs_hero(cls, hero_1, hero_2):
        battle_logs: List[Tuple[int, int]] or List = []
        chances = hero_1.fight_class.statistics.initiative + hero_2.fight_class.statistics.initiative
        finished: bool = False
        winner = None
        loser = None

        if randint(1, chances) <= hero_1.fight_class.statistics.initiative:
            hero_1_attacks = True
        else:
            hero_1_attacks = False

        while not finished:
            if hero_1_attacks:
                battle_log = Battle.__attack(hero_1, hero_2)
                battle_logs.append(battle_log)
                if hero_2.fight_class.statistics.hp <= 0:
                    finished = True
                    winner = hero_1
                    loser = hero_2

            else:
                battle_log = Battle.__attack(hero_2, hero_1)
                battle_logs.append(battle_log)
                if hero_1.fight_class.statistics.hp <= 0:
                    finished = True
                    winner = hero_2
                    loser = hero_1
            hero_1_attacks = not hero_1_attacks

        Battle.__finalize_fight_between_heroes(winner, loser)
        return battle_logs, winner.hero_id

    @classmethod
    def __attack(cls, a, b):
        dmg = randint(1, a.fight_class.baseDmg)
        if not isinstance(a, Bot):
            equipped_weapon = a.eq.itemSlots[9]
            if equipped_weapon is not None:
                dmg *= randint(equipped_weapon.min_dmg, equipped_weapon.max_dmg)
        dmg *= a.strongAgainstOtherClass(b.fight_class)
        dmg = floor(
            dmg / randint(1,
                          b.fight_class.statistics.protection * (1 + b.fight_class.statistics.luck)))
        if dmg > 0:
            b.fight_class.statistics.hp -= dmg
            return -1 if isinstance(a, Bot) else a.hero_id, dmg
        else:
            return -1 if isinstance(a, Bot) else a.hero_id, max(0, dmg)

    @classmethod
    def get_gold_at_stake(cls, hero, other_creature):
        if type(other_creature).__name__ == "Hero":
            return floor((randint(1, 20) / 100) * other_creature.eq.gold * (other_creature.lvl / hero.lvl))
        if type(other_creature).__name__ == "Bot":
            return other_creature.gold

    @classmethod
    def get_exp_at_stake(cls, hero, other_creature):
        if type(other_creature).__name__ == "Hero":
            return floor((other_creature.lvl / hero.lvl) * hero.exp * (randint(1, 1000) / 1000))
        if type(other_creature).__name__ == "Bot":
            return other_creature.gained_exp

    @classmethod
    def __finalize_fight_between_heroes(cls, winner, loser):
        winner.fight_class.statistics.hp = winner.fight_class.statistics.constitution * 100
        loser.fight_class.statistics.hp = loser.fight_class.statistics.constitution * 100

        gold_at_stake = Battle.get_gold_at_stake(winner, loser)
        exp_at_stake = Battle.get_exp_at_stake(winner, loser)

        winner.add_exp(floor(exp_at_stake * randint(1, 26) / 100))

        try:
            conn, cursor = connect_to_db()
            with conn:
                cursor.execute("UPDATE heroes SET gold = gold - %s WHERE hero_id = %s", (gold_at_stake, loser.hero_id))
                cursor.execute("UPDATE heroes SET gold = gold + %s WHERE hero_id = %s", (gold_at_stake, winner.hero_id))
                winner.eq.gold += gold_at_stake
                loser.eq.gold -= gold_at_stake
        except Exception as error:
            print(error)

    @classmethod
    def hero_vs_bot(cls, hero, bot):
        battle_logs: List[Tuple[int, int]] or List = []
        chances = hero.fight_class.statistics.initiative + bot.fight_class.statistics.initiative

        if randint(1, chances) <= hero.fight_class.statistics.initiative:
            hero_attacks = True
        else:
            hero_attacks = False

        while True:
            if hero_attacks:
                battle_log = Battle.__attack(hero, bot)
                battle_logs.append(battle_log)
                if bot.fight_class.statistics.hp <= 0:
                    winner = hero
                    break

            else:
                battle_log = Battle.__attack(bot, hero)
                battle_logs.append(battle_log)
                if hero.fight_class.statistics.hp <= 0:
                    winner = bot
                    break

            hero_attacks = not hero_attacks

        hero.fight_class.statistics.hp = hero.fight_class.statistics.constitution * 100
        bot.fight_class.statistics.hp = bot.fight_class.statistics.constitution * 100

        return battle_logs, -1 if winner is bot else hero.hero_id
