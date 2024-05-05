from dataclasses import dataclass
from justcard.models import Card
from enum import Enum


@dataclass
class GameState:
    deck: list[Card]
    players: list[list[Card]]


class Action(str, Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"


class Stage(Enum):
    FLOP = 1
    TURN = 2
    RIVER = 3
