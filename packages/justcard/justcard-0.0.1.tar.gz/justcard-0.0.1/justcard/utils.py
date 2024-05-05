import asyncio
import random
from functools import lru_cache

from .models import Card, Suit, Rank


@lru_cache
def create_deck() -> list[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]


async def shuffle_deck(deck: list[Card]) -> list[Card]:
    await asyncio.sleep(0)
    random.shuffle(deck)
    return deck
