from justcard.utils import create_deck


def test_create_deck():
    deck = create_deck()
    assert len(deck) == 52, "Deck should have 52 card without the Joker"
