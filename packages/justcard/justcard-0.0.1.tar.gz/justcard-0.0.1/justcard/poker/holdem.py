import random

# Stage: Flop, Turn, River
# Action: Fold, Call, Raise
class Hand(list): ...


def create_deck():
    return []


def draw_card(hand, deck):
    hand.append("DRAW{}".format(random.randint(0, 9)))
    return hand, deck


def main():
    _hands: str = input("Enter number of hands to play: ")
    if not _hands.isdecimal() or int(_hands) <= 0:
        raise TypeError(
            "Number of hands should be integer gather than zero"
        )
    hands: list = [Hand() for _ in range(int(_hands))]
    print(hands)

    # Step 01: Create deck of cards and mark the big buy position
    deck: list = create_deck()

    # Step 02: Give the card to any hands

    for hand in hands:
        _, deck = draw_card(hand, deck)

    print(hands)

    # Step 03: Drop off the card before any step of stages;
    #   Flop -> Action -> Hands exists -> Next
    #   Turn -> Action -> Hands exists -> Next
    #   Raise -> Action -> Hands exists -> Dual the point order of hand


if __name__ == '__main__':
    main()
