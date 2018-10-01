from hand_of_cards import GetCards, GetHandRankings


def test_no_duplicates():
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    test_array_1 = new_hand.hand
    test_array_2 = set(new_hand.hand)
    assert len(test_array_1) == len(test_array_2)


def test_get_pairs():
    hand_ranker = GetHandRankings()
    test_hand_pair = [
        (1, 'C'), (2, 'C'), (4, 'S'),
        (3, 'S'), (4, 'D')
    ]
    test_hand_no_pair = [
        (1, 'C'), (10, 'C'), (4, 'S'),
        (3, 'S'), (9, 'D')
    ]
    assert len(hand_ranker.get_pairs(test_hand_pair)) == 1
    assert hand_ranker.get_pairs(test_hand_no_pair) is None


def test_get_two_pairs():
    hand_ranker = GetHandRankings()
    test_hand_two_pairs = [
        (1, 'C'), (2, 'C'), (4, 'S'),
        (2, 'S'), (4, 'D')
    ]
    test_hand_no_two_pairs = [
        (2, 'C'), (10, 'C'), (4, 'S'),
        (3, 'S'), (4, 'D')
    ]
    assert len(hand_ranker.get_two_pairs(test_hand_two_pairs)) == 2
    assert hand_ranker.get_two_pairs(test_hand_no_two_pairs) is None


def test_three_of_a_kind():
    hand_ranker = GetHandRankings()
    test_hand_no_triples = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (3, 'S'), (9, 'D')
    ]
    test_hand_triples = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (3, 'S'), (10, 'D')
    ]
    assert len(hand_ranker.get_three_of_a_kind(test_hand_triples)) == 3
    assert hand_ranker.get_three_of_a_kind(test_hand_no_triples) is None


def test_four_of_a_kind():
    hand_ranker = GetHandRankings()
    test_hand_no_quads = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (8, 'H'), (10, 'D')
    ]
    test_hand_quads = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (10, 'H'), (10, 'D')
    ]
    assert len(hand_ranker.get_four_of_a_kind(test_hand_quads)) == 4
    assert hand_ranker.get_four_of_a_kind(test_hand_no_quads) is None


def test_full_house():
    hand_ranker = GetHandRankings()
    test_full_house = [
        (10, 'C'), (10, 'D'), (10, 'S'),
        (8, 'H'), (8, 'D')
    ]
    test_no_full_house = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (10, 'H'), (1, 'D')
    ]
    assert hand_ranker.get_full_house(test_full_house) == (10, 10, 10, 8, 8)
    assert hand_ranker.get_full_house(test_no_full_house) is None


def test_straight():
    test_straight = [
        (1, 'C'), (2, 'D'), (3, 'S'),
        (4, 'H'), (5, 'D')
    ]
    test_no_straight = [
        (10, 'C'), (2, 'C'), (10, 'S'),
        (3, 'H'), (1, 'D')
    ]


def test_flush():
    hand_ranker = GetHandRankings()
    test_flush = [
        (10, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (1, 'C')
    ]
    test_no_flush = [
        (10, 'C'), (4, 'C'), (10, 'S'),
        (8, 'C'), (3, 'C')
    ]
    assert hand_ranker.get_flush(test_flush) == ('C')
    assert hand_ranker.get_flush(test_no_flush) is None

def test_straight_flush():
    test_straight_flush = [
        (1, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (4, 'C')
    ]
    test_no_straight_flush = [
        (10, 'C'), (2, 'C'), (5, 'C'),
        (3, 'C'), (1, 'C')
    ]
