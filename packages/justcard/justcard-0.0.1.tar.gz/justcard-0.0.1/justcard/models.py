from dataclasses import dataclass
from enum import Enum, IntEnum
from functools import lru_cache


class Suit(str, Enum):
    """Suit enum
    SPADES = '\u2660'
    HEARTS = '\u2665'
    DIAMONDS = '\u2666'
    CLUBS = '\u2663'
    """

    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"


@lru_cache
def suit_rank(suit: Suit) -> int:
    return {
        "SPADES": 4,
        "HEARTS": 3,
        "DIAMONDS": 2,
        "CLUBS": 1,
    }[suit.name]


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __str__(self) -> str:
        return f"{self.rank.name.capitalize()}{self.suit.value}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank and suit_rank(
                self.suit
            ) == suit_rank(other.suit)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, Card):
            return self.rank > other.rank or (
                self.rank == other.rank
                and suit_rank(self.suit) > suit_rank(other.suit)
            )

    def __ge__(self, other):
        if isinstance(other, Card):
            return self.__gt__(other) or self.__eq__(other)


@dataclass
class GameState:
    deck: list[Card]
    players: list[list[Card]]
