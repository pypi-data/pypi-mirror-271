from justcard.models import Card, Suit, Rank


def test_card():
    first = Card(Suit.SPADES, Rank.FIVE)
    second = Card(Suit.SPADES, Rank.FOUR)
    assert first != second
    assert first >= second
    assert first > second
    assert first == Card(Suit.SPADES, Rank.FIVE)
    assert second == Card(Suit.SPADES, Rank.FOUR)

    first = Card(Suit.SPADES, Rank.FOUR)
    second = Card(Suit.HEARTS, Rank.FOUR)
    assert first != second
    assert first >= second
    assert first > second
