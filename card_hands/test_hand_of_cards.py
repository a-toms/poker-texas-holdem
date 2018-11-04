from hand_of_cards import (
    Player, Players, CardDealer, GetHandRanks, ClassifyHand, FindBestHand,
    GameRound
)
import sys


def test_player():
    pass


def test_players_initialises_with_correct_number_of_players():
    n_players = 8
    for i in range(1, n_players):
        assert hasattr(Players(n_players), f'player{i}') is True


def test_deck_generation_contains_52_cards():
    n_players = 1
    assert len(CardDealer(n_players).deck) == 52


def test_deck_generation_contains_no_duplicate_cards():
    n_players = 5
    new_hand = CardDealer(n_players)
    assert len(new_hand.deck) == len(set(new_hand.deck))


def test_pick_card(): # Todo: rewrite
    n_players = 5
    card_dealer = CardDealer(n_players)
    card = card_dealer.pick_card()
    suites = ('H', 'C', 'S', 'H')
    numbers = [i for i in range(2, 15)]
    assert card[0] in numbers, card[1] in suites


def test_deal_pocket_cards_to_players():
    n_players = 5
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    game_round.deal_pocket_cards_to_players()
    print(game_round.players_information.player1.hand)
    print(game_round.players_information.__dict__)
    for k in game_round.players_information.__dict__:
        print(k)
        print(game_round.players_information.__dict__[k].hand)



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
    assert hand_getter.get_straight_with_low_ace(
        ExampleHands.test_straight) == (1, 2, 3, 4, 5)
    assert hand_getter.get_straight_with_low_ace(
        ExampleHands.test_no_straight) is None
    assert hand_getter.get_straight_without_low_ace(
        ExampleHands.test_ace_high_straight) == (10, 11, 12, 13, 14)
    assert hand_getter.get_straight_without_low_ace(
        ExampleHands.test_no_ace_high_straight) is None
    assert hand_getter.get_straights(
        ExampleHands.test_ace_high_straight) == (10, 11, 12, 13, 14)
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
        (14, 'C'), (11, 'D'), (12, 'S'),
        (10, 'H'), (13, 'D')
    ]
    test_no_ace_high_straight = [
        (10, 'C'), (13, 'C'), (12, 'S'),
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
    sample_hands = [
        test_high_card,
        test_pair,
        test_two_pairs,
        test_triples,
        test_straight,
        test_ace_high_straight,
        test_flush,
        test_full_house,
        test_quads,
        test_straight_flush
    ]
    all_ranked_hands = [
        (1, test_high_card),
        (2, test_pair),
        (3, test_two_pairs),
        (4, test_triples),
        (5, test_straight),
        (5, test_ace_high_straight),
        (6, test_flush),
        (7, test_full_house),
        (8, test_quads),
        (9, test_straight_flush)
    ]
    high_card_ranked_hands = [
        (1, [(12, 'H'), (10, 'C'), (3, 'C'), (4, 'S'), (2, 'H')]),
        (1, [(12, 'C'), (9, 'C'), (7, 'S'), (5, 'C'), (6, 'H'), ]),
        (1, [(12, 'D'), (2, 'C'), (7, 'D'), (4, 'D'), (8, 'C')]),
        (1, [(12, 'S'), (2, 'S'), (7, 'C'), (4, 'H'), (8, 'H')]),
        (1, [(11, 'D'), (2, 'D'), (7, 'H'), (4, 'C'), (8, 'S')]),
    ]
    full_house_ranked_hands = [
        # 12H, 12C, 6S, 7C and 8H on the board. 5 players
        (3, [(12, 'H'), (12, 'C'), (8, 'H'), (3, 'S'), (3, 'C')]),  # pocket 3s
        (2, [(12, 'H'), (12, 'C'), (6, 'S'), (7, 'C'), (8, 'H'), ]),  # 2D, 3H
        (2, [(12, 'H'), (12, 'C'), (10, 'D'), (9, 'D'), (8, 'H')]),  # 10D, 9D
        (7, [(12, 'H'), (12, 'C'), (12, 'D'), (8, 'C'), (8, 'H')]),  # 12D , 8C
        (7, [(11, 'H'), (12, 'C'), (12, 'S'), (7, 'C'), (7, 'S')])  # 12S, 7S
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
        ExampleHands.test_straight_flush) == hand_and_rank['straight flush']
    assert hand_classifier.rank_hand(
        ExampleHands.test_quads) == hand_and_rank['four of a kind']
    assert hand_classifier.rank_hand(
        ExampleHands.test_full_house) == hand_and_rank['full house']
    assert hand_classifier.rank_hand(
        ExampleHands.test_flush) == hand_and_rank['flush']
    assert hand_classifier.rank_hand(
        ExampleHands.test_straight) == hand_and_rank['straight']
    assert hand_classifier.rank_hand(
        ExampleHands.test_triples) == hand_and_rank['three of a kind']
    assert hand_classifier.rank_hand(
        ExampleHands.test_two_pairs) == hand_and_rank['two pairs']
    assert hand_classifier.rank_hand(
        ExampleHands.test_pair) == hand_and_rank['pair']
    assert hand_classifier.rank_hand(
        ExampleHands.test_high_card) == hand_and_rank['high card']


def test_ranks_hands():
    assert ClassifyHand().rank_hands(
        ExampleHands().sample_hands) == ExampleHands().all_ranked_hands


def test_get_highest_rank():
    assert FindBestHand().get_highest_rank(
        ExampleHands().all_ranked_hands) == 9


def test_get_card_numbers_sorted_by_frequency_and_size():
    card_numbers1 = [3, 5, 3, 12, 12]
    card_numbers2 = [14, 14, 2, 2, 2]
    assert FindBestHand().sort_by_frequency_and_size(
        card_numbers1) == [12, 12, 3, 3, 5]
    assert FindBestHand().sort_by_frequency_and_size(
        card_numbers2) == [2, 2, 2, 14, 14]


def test1_get_card_numbers_from_highest_ranked_cards():
    #     3H, 3C, 4S, 14C and 8H on the board. 5 players
    #     board = [(3, 'H'), (3, 'C'), (4, 'S'), (14, 'C'), (8, 'H')]
    test_ranked_hand = [
        (3, [(2, 'H'), (2, 'C'), (3, 'H'), (14, 'C'), (3, 'C')]),  # pocket 2s
        (2, [(3, 'H'), (3, 'C'), (6, 'H'), (14, 'C'), (8, 'H')]),  # 2D, 6H
        (3, [(3, 'H'), (4, 'D'), (4, 'S'), (14, 'C'), (14, 'D')]),  # 14D, 4D
        (3, [(3, 'H'), (3, 'C'), (8, 'C'), (14, 'C'), (8, 'H')]),  # 12D , 8C
        (2, [(3, 'H'), (3, 'C'), (12, 'S'), (14, 'C'), (8, 'H')])  # 12S, 7S
    ]
    assert FindBestHand().get_card_numbers_from_highest_ranked_cards(
        test_ranked_hand) == [
        [3, 3, 2, 2, 14], [14, 14, 4, 4, 3], [8, 8, 3, 3, 14]
    ]


def test2_get_card_numbers_from_highest_ranked_cards():
    assert len(FindBestHand().get_card_numbers_from_highest_ranked_cards(
        ExampleHands().high_card_ranked_hands)) == 5
    assert len(FindBestHand().get_card_numbers_from_highest_ranked_cards(
        ExampleHands().full_house_ranked_hands)) == 2
    assert len(FindBestHand().get_card_numbers_from_highest_ranked_cards(
        ExampleHands().all_ranked_hands)) == 1


def test_get_winner_from_same_ranked_hands():
    two_pairs = [
        (3, 3, 2, 2, 14), (14, 14, 4, 4, 3), (8, 8, 3, 3, 14), (8, 8, 3, 3, 14)
    ]
    best_of_two_pairs = (14, 14, 4, 4, 3)
    assert FindBestHand().get_highest_card(two_pairs) == best_of_two_pairs


# Discuss this aspect with J: is it better to have a single class
# containing the model data? Would require the test data to be reset frequently


def test_game_round_instantiates_to_include_players_class_instantiation():
    all_players = Players(6)
    card_dealer = CardDealer(6)
    game_round = GameRound(all_players, card_dealer)
    assert type(game_round.players_information.player1.money) is int


def test_pay_blinds():
    n_players = 3
    all_players = Players(3)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    starting_player_money = 100
    starting_player_amount_bet = 0
    assert game_round.big_blind_player == 'player3'
    assert game_round.players_information.player3.money == starting_player_money
    assert game_round.players_information.player3.amount_bet_in_round == starting_player_amount_bet
    assert game_round.small_blind_player == 'player2'
    assert game_round.players_information.player2.money == starting_player_money
    assert game_round.players_information.player3.amount_bet_in_round == starting_player_amount_bet
    game_round.pay_blinds()
    assert game_round.players_information.player3.money == starting_player_money - game_round.big_blind
    assert game_round.players_information.player3.amount_bet_in_round == starting_player_amount_bet + game_round.big_blind
    assert game_round.players_information.player2.money == starting_player_money - game_round.small_blind
    assert game_round.players_information.player2.amount_bet_in_round == starting_player_amount_bet + game_round.small_blind
    assert game_round.pot == game_round.big_blind + game_round.small_blind
    assert game_round.highest_round_bet == game_round.big_blind


def test_pre_flop_playing_order():
    n_players = 8
    all_players = Players(8)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    assert game_round.big_blind_player == 'player8'
    assert game_round.pre_flop_playing_order[-1] == 'player8'
    assert game_round.small_blind_player == 'player7'
    assert game_round.pre_flop_playing_order[-2] == 'player7'
    assert game_round.dealer_player == 'player6'
    assert game_round.pre_flop_playing_order[-3] == 'player6'


def test_post_flop_playing_order():
    n_players = 8
    all_players = Players(8)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    assert game_round.big_blind_player == 'player8'
    assert game_round.post_flop_playing_order[1] == 'player8'
    assert game_round.small_blind_player == 'player7'
    assert game_round.post_flop_playing_order[0] == 'player7'
    assert game_round.dealer_player == 'player6'
    assert game_round.post_flop_playing_order[-1] == 'player6'


def test_call_bet_successful():
    n_players = 6
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    game_round.pay_blinds()
    start_money = game_round.players_information.__dict__['player3'].money
    game_round.call_bet('player3')
    post_call_money = game_round.players_information.__dict__['player3'].money
    assert post_call_money < start_money
    assert start_money - post_call_money == game_round.big_blind

def test_call_bet_unsuccessful():
    n_players = 6
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    game_round.players_information.__dict__['player1'].money = 50
    game_round.highest_round_bet = 100
    assert game_round.call_bet('player1') is False



def test_fold_hand():
    n_players = 5
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    assert game_round.player_position_order[3] == 'player4'
    assert game_round.pre_flop_playing_order[3] == 'player4'
    assert game_round.post_flop_playing_order[0] == 'player4'  # After blinds paid
    game_round.fold_hand('player4')
    assert game_round.player_position_order[3] == 'player4'  # Unaffected by fold
    assert game_round.pre_flop_playing_order[3] == 'player5'
    assert game_round.post_flop_playing_order[0] == 'player5'
    assert 'player4' not in game_round.pre_flop_playing_order
    assert 'player4' not in game_round.post_flop_playing_order


def test_player_chooses_check_bet(monkeypatch):
    n_players = 6
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    game_round.highest_round_bet = 50
    game_round.players_information.__dict__['player1'].amount_bet_in_round = 50
    monkeypatch.setattr('builtins.input', lambda x: 0)
    assert game_round.check_bet('player1') is True

# How do I test the perform bet action?

def test_player_chooses_call_bet(monkeypatch):
    n_players = 6
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    monkeypatch.setattr('builtins.input', lambda x: 1)
    i = int(input(''))
    assert i == 1
    game_round.highest_round_bet = 50
    game_round.players_information.__dict__['player1'].money = 100
    assert game_round.call_bet('player1') is True



def test_give_pot_to_winners():
    n_players = 7
    game_round = GameRound(Players(n_players), CardDealer(n_players))
    game_round.pot = 150
    winners = ('player1', 'player2')
    game_round.players_information.player1.money = 100
    game_round.players_information.player2.money = 100
    game_round.give_pot_to_winners(winners)
    assert game_round.players_information.player1.money == 175
    assert game_round.players_information.player2.money == 175
    assert game_round.pot == 0
    game_round.pot = 200
    winner = ('player3',)
    game_round.players_information.player3.money = 100
    game_round.give_pot_to_winners(winner)
    assert game_round.players_information.player3.money == 300
    assert game_round.pot == 0


class TestGetPlayerCommands:
    n_players = 2
    all_players = Players(n_players)
    card_dealer = CardDealer(n_players)
    game_round = GameRound(all_players, card_dealer)
    player_1 = game_round.players_information.__dict__['player1']
    player_1.money = 100

    def test_get_player_commands(self, monkeypatch):
        # Monkeypatch simulates the user entering input in the terminal.
        monkeypatch.setattr('builtins.input', lambda x: 'some input')
        pass




