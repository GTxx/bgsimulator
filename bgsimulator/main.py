import random

from enum import Enum
from typing import Optional, Tuple, Union

from bgsimulator.context import battleground


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


POISON_ATTACK = "POISON"

def normal_attack(minion1: 'Minion', minion2: 'Minion'):
    minion2.be_attacked(minion1.attack_val)
    minion1.be_attacked(minion2.attack_val)


def sweep_attack(minion1: 'Minino', minion2: 'Minion'):
    pass



class Minion:
    def __init__(self, attack: Union[int, str], blood, name="", minion_type= MinionType.NEUTRAL, description="", taunt=False, divien_shield=False):
        self.trie = int
        self.is_gold = False
        self.attack_val = attack
        self.blood = blood
        self.status = "live"
        self.pick_attack_object_strategy = None
        self.description = description
        self.name = name
        self.taunt = taunt
        self.divien_shield = False
        self.minion_type = minion_type

    @classmethod
    def fuse_to_gold(cls, minion1: 'Minion', minion2: 'Minion', minion3: 'Minion'):
        pass

    def pick_attack_object(self, side: 'Side') -> 'Minion':
        if self.pick_attack_object_strategy:
            return self.pick_attack_object_strategy()
        else:
            taunt_minions = [minion for minion in side.minions if minion.taunt]
            if taunt_minions:
                return random.choice(taunt_minions)
            else:
                return random.choice(side.minions)

    def attack(self, minion: 'Minion'):
        battleground.get().replay.record(f"{self} attack {minion}")
        self.be_attacked(minion.attack_val)
        minion.be_attacked(self.attack_val)

    def be_attacked(self, attack_val):
        if self.divien_shield:
            self.divien_shield = False
        if attack_val == POISON_ATTACK:
            self.blood = 0
        else:
            self.blood -= attack_val
        if self.blood <= 0:
            self.status = 'dead'

    def __str__(self):
        return f"{self.name if self.name else 'DUMMY'}:{self.attack_val}/{self.blood}"


class Hero:
    def __init__(self, name="", blood=1):
        self.blood = 1
        self.name = name

    def __str__(self):
        return f"{self.name}/{self.blood}"


DUMMY_HERO1 = Hero("Hero1")
DUMMY_HERO2 = Hero("Hero2")


class Deathrattle:
    def __init__(self, priority, action):
        self.priority = priority
        self.action = action

    def __ge__(self, other):
        return self.priority >= other.priority


class Replay:
    def __init__(self, view):
        self.view = view
        self.records = []

    def record(self, s):
        self.records.append(s)
        self.view(s)

    def play(self):
        for s in self.records:
            print(s)


DUMMY_REPLAY = Replay(lambda s: s)


class Side:
    def __init__(self, hero: Hero, *minion_list: Minion):
        self.minions = minion_list
        self.active_minion_idx = 0
        self.hero = hero

    def is_empty(self) -> bool:
        return not self.minions

    def next_active_minion(self) -> Optional[Minion]:
        return self.minions[self.active_minion_idx]

    def __str__(self):
        return f"{self.hero}>{self.minions}"

class BattleGround:
    def __init__(self, side1: Side, side2: Side, replay: Replay = DUMMY_REPLAY):
        self.side1 = side1
        self.side2 = side2
        self.replay = replay
        self.active_side = random.choice([side1, side2])

    def next_active_side(self) -> Tuple[Side, Side]:
        if self.active_side is self.side1:
            self.active_side = self.side2
            return self.side2, self.side1
        else:
            self.active_side = self.side1
            return self.side1, self.side2

    def start(self):
        while not self.side1.is_empty() and not self.side2.is_empty():
            action_side, other_side = self.next_active_side()
            minion = action_side.next_active_minion()
            attack_object = minion.pick_attack_object(other_side)
            minion.attack(attack_object)

            # remove death minion and trigger deathrattle
            death_minions = []
            for minion in action_side.minions:
                if minion.blood <= 0:
                    death_minions.append(minion)
            for minion in other_side.minions:
                if minion.blood <= 0:
                    death_minions.append(minion)
            # TODO: trigger deathrattle

            action_side.minions = [minion for minion in action_side.minions if minion.blood > 0]
            other_side.minions = [minion for minion in other_side.minions if minion.blood > 0]

    def get_other_side(self, minion: Minion) -> Side:
        if minion in self.side1.minions:
            return self.side2
        else:
            return self.side1
