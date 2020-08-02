from bgsimulator.main import Side, DUMMY_HERO2, Minion, DUMMY_HERO1, setup_battleground, POISON_ATTACK


def test_poisonous():
    side1 = Side(DUMMY_HERO2, Minion(POISON_ATTACK, 2))
    side2 = Side(DUMMY_HERO1, Minion(1, 10000))

    with setup_battleground(side1, side2) as bg:
        bg.start()
        assert bg.side2.is_empty()
        assert not bg.side1.is_empty()
        bg.replay.play()