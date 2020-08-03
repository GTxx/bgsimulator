from _contextvars import ContextVar
from contextlib import contextmanager

from bgsimulator.main import DUMMY_REPLAY, BattleGround


@contextmanager
def setup_battleground(side1, side2, replay=DUMMY_REPLAY):
    bg = BattleGround(side1, side2, replay)
    token = battleground.set(bg)
    yield bg
    battleground.reset(token)


battleground: ContextVar[BattleGround] = ContextVar("battleground")