from bgsimulator.main import Minion, Side, DUMMY_HERO1, DUMMY_HERO2
from bgsimulator.context import setup_battleground


def test_taunt():
    side1 = Side(DUMMY_HERO2, Minion(2, 1))

    taunt_minion = Minion(2, 2, taunt=True)
    no_taunt_minion = Minion(1, 1)
    side2 = Side(DUMMY_HERO1, taunt_minion, no_taunt_minion)

    with setup_battleground(side1, side2) as bg:
        bg.start()
        assert bg.side1.is_empty()
        assert not bg.side2.is_empty()
        assert bg.side2.minions[0] is no_taunt_minion
        bg.replay.play()
