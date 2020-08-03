from bgsimulator.main import Minion, Side, DUMMY_HERO
from bgsimulator.context import setup_battleground


class FooMinion(Minion):
    def __init__(self):
        pass


def test_basic_minion_battle_1v1():
    with setup_battleground(Side(DUMMY_HERO, Minion(1,1)), Side(DUMMY_HERO, Minion(2, 2))) as bg:
        bg.start()
        assert bg.side1.is_empty()
        bg.replay.play()


def test_basic_battle_2v2():
    side1 = Side(DUMMY_HERO, Minion(2,2), Minion(2,2))
    side2 = Side(DUMMY_HERO, Minion(2, 1), Minion(2,2))
    with setup_battleground(side1, side2) as bg:
        bg.start()
        assert bg.side1.is_empty() and bg.side2.is_empty()
