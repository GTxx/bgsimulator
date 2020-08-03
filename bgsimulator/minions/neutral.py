from bgsimulator.main import MinionType, Minion
from bgsimulator.context import battleground
import random


ZappSlywick = Minion(7, 10, "ZappSlywick", description="Windfury This minion always attacks the enemy minion with the lowest Attack.")


def windfurry_attack(minion):
    # pick the enemy minion with lowest attack
    side = battleground.get().get_other_side(minion)
    attack_vals = [minion.attack_val for minion in side.minions]
    min_attack_val = min(attack_vals)
    attack_minion = random.choice([minion for minion in side.minions if minion.attack_val == min_attack_val])

    # do attack

    #
