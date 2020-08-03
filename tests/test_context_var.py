
from bgsimulator.main import Side, Minion
from bgsimulator.context import setup_battleground, battleground


def test_build_battlground_context():
    side1 = Side([Minion(1, 1)])
    side2 = Side([Minion(2, 2)])
    with setup_battleground(side1, side2):
        def inner():
            with setup_battleground(Side([Minion(3, 3)]), Side([Minion(4, 4)])):
                assert battleground.get().side1.minions[0].attack_val == 3
                assert battleground.get().side2.minions[0].attack_val == 4
                assert battleground.get().side1.minions[0].blood == 3
                assert battleground.get().side2.minions[0].blood == 4
        inner()
        assert battleground.get().side1.minions[0].attack_val == 1
        assert battleground.get().side2.minions[0].attack_val == 2
        assert battleground.get().side1.minions[0].blood == 1
        assert battleground.get().side2.minions[0].blood == 2
