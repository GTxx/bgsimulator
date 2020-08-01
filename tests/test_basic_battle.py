from bgsimulator.main import Minion, setup_battleground, Side, DUMMY_HERO


class FooMinion(Minion):
    def __init__(self):
        pass


def test_2_basic_minion_battle():
    with setup_battleground(Side([Minion(1,1)], DUMMY_HERO), Side([Minion(2, 2)], DUMMY_HERO)) as bg:
        bg.start()
        assert bg.side1.is_empty()
