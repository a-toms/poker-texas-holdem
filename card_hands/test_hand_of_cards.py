from hand_of_cards import GetCards, GetHandRanks, ClassifyHand


def test_no_duplicates():
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    test_array_1 = new_hand.hand
    test_array_2 = set(new_hand.hand)
    assert len(test_array_1) == len(test_array_2)


def test_get_high_card():
    hand_getter = GetHandRanks()
    assert hand_getter.get_high_card(ExampleHands.test_high_card) == (
        1, 2, 3, 4, 7
    )


def test_get_pairs():
    hand_getter = GetHandRanks()
    assert len(hand_getter.get_pairs(ExampleHands.test_pair)) == 1
    assert hand_getter.get_pairs(ExampleHands.test_no_pair) is None


def test_get_two_pairs():
    hand_getter = GetHandRanks()
    assert len(hand_getter.get_two_pairs(
        ExampleHands.test_two_pairs)) == 2
    assert hand_getter.get_two_pairs(
        ExampleHands.test_no_two_pairs) is None


def test_three_of_a_kind():
    hand_getter = GetHandRanks()
    assert len(hand_getter.get_three_of_a_kind(
        ExampleHands.test_triples)) == 3
    assert hand_getter.get_three_of_a_kind(
        ExampleHands.test_no_triples) is None


def test_four_of_a_kind():
    hand_getter = GetHandRanks()
    assert len(hand_getter.get_four_of_a_kind(
        ExampleHands.test_quads)) == 4
    assert hand_getter.get_four_of_a_kind(
        ExampleHands.test_no_quads) is None


def test_full_house():
    hand_getter = GetHandRanks()
    assert hand_getter.get_full_house(
        ExampleHands.test_full_house) == (10, 10, 10, 8, 8)
    assert hand_getter.get_full_house(
        ExampleHands.test_no_full_house) is None


def test_straight():
    hand_getter = GetHandRanks()
    assert hand_getter.get_straight_with_no_ace_high(
        ExampleHands.test_straight) == (1, 2, 3, 4, 5)
    assert hand_getter.get_straight_with_no_ace_high(
        ExampleHands.test_no_straight) is None
    assert hand_getter.get_ace_high_straight(
        ExampleHands.test_ace_high_straight) == (9, 10, 11, 12, 13)
    assert hand_getter.get_ace_high_straight(
        ExampleHands.test_no_ace_high_straight) is None
    assert hand_getter.get_straights(
        ExampleHands.test_ace_high_straight) == (9, 10, 11, 12, 13)
    assert hand_getter.get_straights(
        ExampleHands.test_straight) == (1, 2, 3, 4, 5)
    assert hand_getter.get_straights(ExampleHands.test_no_straight) is None
    assert hand_getter.get_straights(ExampleHands.test_no_straight2) is None


def test_flush():
    hand_getter = GetHandRanks()
    assert hand_getter.get_flush(ExampleHands.test_flush) == 'C'
    assert hand_getter.get_flush(ExampleHands.test_no_flush) is None


def test_straight_flush():
    hand_getter = GetHandRanks()
    assert hand_getter.get_straight_flush(
        ExampleHands.test_straight_flush) == [
            (1, 'C'), (2, 'C'), (3, 'C'),
            (4, 'C'), (5, 'C')
    ]
    assert hand_getter.get_straight_flush(
        ExampleHands.test_no_straight_flush) is None


class ExampleHands:
    test_high_card = [
        (1, 'C'), (2, 'C'), (4, 'S'),
        (3, 'S'), (7, 'D')
    ]
    test_pair = [
        (1, 'C'), (2, 'C'), (4, 'S'),
        (3, 'S'), (4, 'D')
    ]
    test_no_pair = [
        (1, 'C'), (10, 'C'), (4, 'S'),
        (3, 'S'), (9, 'D')
    ]
    test_two_pairs = [
        (1, 'C'), (2, 'C'), (4, 'S'),
        (2, 'S'), (4, 'D')
    ]
    test_no_two_pairs = [
        (2, 'C'), (10, 'C'), (4, 'S'),
        (3, 'S'), (4, 'D')
    ]
    test_no_triples = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (3, 'S'), (9, 'D')
    ]
    test_triples = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (3, 'S'), (10, 'D')
    ]
    test_straight = [
        (5, 'C'), (3, 'D'), (2, 'S'),
        (4, 'H'), (1, 'D')
    ]
    test_no_straight = [
        (10, 'C'), (7, 'C'), (10, 'S'),
        (9, 'H'), (1, 'D')
    ]
    test_no_straight2 = [
        (5, 'C'), (3, 'D'), (3, 'S'),
        (4, 'H'), (1, 'D')
    ]
    test_ace_high_straight = [
        (1, 'C'), (11, 'D'), (12, 'S'),
        (9, 'H'), (10, 'D')
    ]
    test_no_ace_high_straight = [
        (10, 'C'), (8, 'C'), (9, 'S'),
        (11, 'H'), (1, 'D')
    ]
    test_flush = [
        (10, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (1, 'C')
    ]
    test_no_flush = [
        (10, 'C'), (4, 'C'), (10, 'S'),
        (8, 'C'), (3, 'C')
    ]
    test_full_house = [
        (10, 'C'), (10, 'D'), (10, 'S'),
        (8, 'H'), (8, 'D')
    ]
    test_no_full_house = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (10, 'H'), (1, 'D')
    ]
    test_no_quads = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (8, 'H'), (10, 'D')
    ]
    test_quads = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (10, 'H'), (10, 'D')
    ]
    test_straight_flush = [
        (1, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (4, 'C')
    ]
    test_no_straight_flush = [
        (10, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (1, 'C')
    ]


def test_classify_hand():
    """Check that rank numbers are correctly output for each hand"""
    hand_classifier = ClassifyHand()
    hand_and_rank = {
        'straight flush': 9,
        'four of a kind': 8,
        'full house': 7,
        'flush': 6,
        'straight': 5,
        'three of a kind': 4,
        'two pairs': 3,
        'pair': 2,
        'high card': 1
    }
    assert hand_classifier.rank_hand(
        ExampleHands.test_straight_flush)[0] == hand_and_rank['straight flush']
    assert hand_classifier.rank_hand(
        ExampleHands.test_quads)[0] == hand_and_rank['four of a kind']
    assert hand_classifier.rank_hand(
        ExampleHands.test_full_house)[0] == hand_and_rank['full house']
    assert hand_classifier.rank_hand(
        ExampleHands.test_flush)[0] == hand_and_rank['flush']
    assert hand_classifier.rank_hand(
        ExampleHands.test_straight)[0] == hand_and_rank['straight']
    assert hand_classifier.rank_hand(
        ExampleHands.test_triples)[0] == hand_and_rank['three of a kind']
    assert hand_classifier.rank_hand(
        ExampleHands.test_two_pairs)[0] == hand_and_rank['two pairs']
    assert hand_classifier.rank_hand(
        ExampleHands.test_pair)[0] == hand_and_rank['pair']
    assert hand_classifier.rank_hand(
        ExampleHands.test_high_card)[0] == hand_and_rank['high card']