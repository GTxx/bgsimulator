from _contextvars import ContextVar
from contextlib import contextmanager
import random

from enum import Enum
from typing import Optional, List, Tuple


class Card:
    def __init__(self, minion: 'Minion'):
        self.minion = minion

class MinionType(Enum):
    BEAST = 1
    DEMON = 2
    DRAGON = 3
    MECH = 4
    MURLOC = 5
    PIRATE = 6
    NEUTRAL = 7


class Minion:
    def __init__(self, attack, blood, name="", description=""):
        self.trie = int
        self.is_gold = False
        self.attack_val = attack
        self.blood = blood
        self.status = "live"
        self.pick_attack_object_strategy = None
        self.description = description
        self.name = name

    @classmethod
    def fuse_to_gold(cls, minion1: 'Minion', minion2: 'Minion', minion3: 'Minion'):
        pass

    def pick_attack_object(self, side: 'Side') -> 'Minion':
        if self.pick_attack_object_strategy:
            return self.pick_attack_object_strategy()
        else:
            return random.choice(side.minions)

    def attack(self, minion: 'Minion'):
        if minion.attack_val >= self.blood:
            self.blood = 0
            self.status = "dead"
        else:
            self.blood = self.blood - minion.attack_val

        if self.attack_val >= minion.blood:
            minion.blood = 0

class Hero:
    pass


DUMMY_HERO = Hero()


class Alleycat(Minion):
    def __init__(self):
        pass


class Deathrattle:
    pass


class Side:
    def __init__(self, minion_list: List, hero: Hero):
        self.minions = minion_list
        self.active_minion_idx = 0
        self.hero = hero

    def is_empty(self) -> bool:
        return not self.minions

    def next_active_minion(self) -> Optional[Minion]:
        return self.minions[self.active_minion_idx]


class BattleGround:
    def __init__(self, side1: Side, side2: Side):
        self.side1 = side1
        self.side2 = side2
        self.active_side = random.choice([side1, side2])

    def next_active_side(self) -> Tuple[Side, Side]:
        if self.active_side is self.side1:
            self.active_side = self.side2
            return self.side2, self.side1
        else:
            self.active_side = self.side1
            return self.side1, self.side2

    def start(self):
        while not self.side1.is_empty() and not self.side1.is_empty():
            side, other_side = self.next_active_side()
            minion = side.next_active_minion()
            attack_object = minion.pick_attack_object(other_side)
            minion.attack(attack_object)

            side.minions = [minion for minion in side.minions if minion.blood > 0]
            other_side.minions = [minion for minion in other_side.minions if minion.blood > 0]


@contextmanager
def setup_battleground(side1, side2):
    bg = BattleGround(side1, side2)
    token = battleground.set(BattleGround(side1, side2))
    yield bg
    battleground.reset(token)


battleground: ContextVar[BattleGround] = ContextVar("battleground")