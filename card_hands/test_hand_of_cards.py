from hand_of_cards import (
    Player, Players, CardDealer, GetHandRanks, ClassifyHand, FindBestHand,
    GameRound
)
import unittest


class TestDealingCards(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.game_round = GameRound(Players(n_players), CardDealer(n_players))
        self.players_information = self.game_round.players_information
        self.suites = ('H', 'C', 'S', 'D')
        self.numbers = [i for i in range(2, 15)]

    def test_52_cards_in_deck(self):
        self.assertIs(52, len(self.game_round.card_dealer.deck))

    def test_pick_card(self):
        card = self.game_round.card_dealer.pick_card()
        self.assertIn(card[0], self.numbers)
        self.assertIn(card[1], self.suites)

    def test_deal_pocket_cards_to_players(self):
        self.game_round.deal_pocket_cards_to_players()
        self.assertIn('player8', self.players_information.__dict__.keys())
        self.assertEqual(
            str, type(self.players_information.player8.hand[1][1])
        )
        self.assertEqual(
            int, type(self.players_information.player8.hand[1][0])
        )


class TestHandRankingSystem(unittest.TestCase):
    def setUp(self):
        self.ranker = GetHandRanks()

    def test_get_high_card(self):
        assert self.ranker.get_high_card(ExampleHands.test_high_card) == (
            1, 2, 3, 4, 7
        )

    def test_get_pairs(self):
        self.assertEqual(len(self.ranker.get_pairs(ExampleHands.test_pair)), 1)
        self.assertIsNone(self.ranker.get_pairs(ExampleHands.test_no_pair))

    def test_get_two_pairs(self):
        self.assertEqual(
            len(self.ranker.get_two_pairs(ExampleHands.test_two_pairs)), 2
        )
        self.assertIsNone(
            self.ranker.get_two_pairs(ExampleHands.test_no_two_pairs)
        )

    def test_three_of_a_kind(self):
        self.assertEqual(
            len(self.ranker.get_three_of_a_kind(ExampleHands.test_triples)), 3
        )
        self.assertIsNone(
            self.ranker.get_three_of_a_kind(ExampleHands.test_no_triples)
        )

    def test_four_of_a_kind(self):
        self.assertEqual(
            len(self.ranker.get_four_of_a_kind(ExampleHands.test_quads)), 4
        )
        self.assertIsNone(
            self.ranker.get_four_of_a_kind(ExampleHands.test_no_quads)
        )

    def test_full_house(self):
        self.assertEqual(
            self.ranker.get_full_house(ExampleHands.test_full_house),
            (10, 10, 10, 8, 8)
        )
        self.assertIsNone(
            self.ranker.get_full_house(ExampleHands.test_no_full_house)
        )

    def test_straight(self):
        self.assertEqual(
            self.ranker.get_straight_with_low_ace(ExampleHands.test_straight),
            (1, 2, 3, 4, 5)
        )
        self.assertIsNone(self.ranker.get_straight_with_low_ace(
            ExampleHands.test_no_straight)
        )
        self.assertEqual(
            self.ranker.get_straight_without_low_ace(
                ExampleHands.test_ace_high_straight),
            (10, 11, 12, 13, 14)
        )
        self.assertIsNone(self.ranker.get_straight_without_low_ace(
            ExampleHands.test_no_ace_high_straight)
        )
        self.assertEqual(
            self.ranker.get_straights(ExampleHands.test_ace_high_straight),
            (10, 11, 12, 13, 14)
        )
        self.assertEqual(
            self.ranker.get_straights(ExampleHands.test_straight),
            (1, 2, 3, 4, 5)
        )
        self.assertIsNone(
            self.ranker.get_straights(ExampleHands.test_no_straight)
        )
        self.assertIsNone(
            self.ranker.get_straights(ExampleHands.test_no_straight2)
        )

    def test_flush(self):
        self.assertEqual(self.ranker.get_flush(ExampleHands.test_flush), 'C')
        self.assertIsNone(self.ranker.get_flush(ExampleHands.test_no_flush))

    def test_straight_flush(self):
        self.assertEqual(self.ranker.get_straight_flush(
            ExampleHands.test_straight_flush),
            [(1, 'C'), (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C')]
        )
        self.assertIsNone(
            self.ranker.get_straight_flush(ExampleHands.test_no_straight_flush)
        )


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


class TestHandClassifier(unittest.TestCase):
    """
    Check that rank numbers are correctly output for each hand.
    """
    def setUp(self):
        self.hand_classifier = ClassifyHand()
        self.hand_and_rank = {
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

    def check_straight_flush(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_straight_flush),
            self.hand_and_rank['straight flush']
        )

    def check_quads(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_quads),
            self.hand_and_rank['four of a kind']
        )

    def check_full_house(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_full_house),
            self.hand_and_rank['full house']
        )

    def check_flush_classifier(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_flush),
            self.hand_and_rank['flush']
        )

    def check_straight(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_straight),
            self.hand_and_rank['straight']
        )

    def check_triples(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_triples),
            self.hand_and_rank['three of a kind']
        )

    def check_two_pairs(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_two_pairs),
            self.hand_and_rank['two pairs']
        )

    def check_paid(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_pair),
            self.hand_and_rank['pair']
        )

    def check_high_card(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_high_card),
            self.hand_and_rank['high card']
        )

    def check_all_hands(self):
        self.assertEqual(
            ClassifyHand().rank_hands(ExampleHands().sample_hands),
            ExampleHands().all_ranked_hands
        )


class TestFindBestHand(unittest.TestCase):

    def setUp(self):
        self.find_best_hand = FindBestHand()

    def test_get_highest_rank(self):
        self.assertEqual(
            self.find_best_hand.get_highest_rank(ExampleHands().all_ranked_hands),
            9
        )

    def test_get_card_numbers_sorted_by_frequency_and_size_higher_size(self):
        card_numbers = [3, 5, 3, 12, 12]
        self.assertEqual(
            self.find_best_hand.sort_by_frequency_and_size(card_numbers),
            [12, 12, 3, 3, 5]
        )

    def test_get_card_numbers_sorted_by_frequency_and_size_higher_frequency(self):
        card_numbers = [14, 14, 2, 2, 2]
        self.assertEqual(
            self.find_best_hand.sort_by_frequency_and_size(card_numbers),
            [2, 2, 2, 14, 14]
        )

    def test1_get_card_numbers_from_cards_in_highest_rank(self):
        """
        3H, 3C, 4S, 14C and 8H on the board. 5 players.
        board = [(3, 'H'), (3, 'C'), (4, 'S'), (14, 'C'), (8, 'H')].
        The test_hand is ranked.
        """
        test_hand = [
            (3, [(2, 'H'), (2, 'C'), (3, 'H'), (14, 'C'), (3, 'C')]),  # pocket 2s
            (2, [(3, 'H'), (3, 'C'), (6, 'H'), (14, 'C'), (8, 'H')]),  # 2D, 6H
            (3, [(3, 'H'), (4, 'D'), (4, 'S'), (14, 'C'), (14, 'D')]),  # 14D, 4D
            (3, [(3, 'H'), (3, 'C'), (8, 'C'), (14, 'C'), (8, 'H')]),  # 12D , 8C
            (2, [(3, 'H'), (3, 'C'), (12, 'S'), (14, 'C'), (8, 'H')])  # 12S, 7S
        ]
        self.assertEqual(
            self.find_best_hand.get_card_numbers_from_cards_in_highest_rank(test_hand),
            [[3, 3, 2, 2, 14], [14, 14, 4, 4, 3], [8, 8, 3, 3, 14]]
        )

    def test2_get_card_numbers_from_highest_ranked_cards(self):
        self.assertEqual(
            len(self.find_best_hand.get_card_numbers_from_cards_in_highest_rank(
                ExampleHands().high_card_ranked_hands)),
            5
        )

    def test3_get_card_numbers_from_highest_ranked_cards(self):
        self.assertEqual(
            len(self.find_best_hand.get_card_numbers_from_cards_in_highest_rank(
                ExampleHands().full_house_ranked_hands)),
            2
        )

    def test4_get_card_numbers_from_highest_ranked_cards(self):
        self.assertEqual(
            len(self.find_best_hand.get_card_numbers_from_cards_in_highest_rank(
                ExampleHands().all_ranked_hands)),
            1
        )

    def test_get_winner_from_same_ranked_hands(self):
        two_pairs = [
            (3, 3, 2, 2, 14), (14, 14, 4, 4, 3), (8, 8, 3, 3, 14),
            (8, 8, 3, 3, 14)
        ]
        best_of_two_pairs = (14, 14, 4, 4, 3)
        self.assertEqual(
            self.find_best_hand.get_highest_card(two_pairs),
            best_of_two_pairs
        )


def test_game_round_instantiates_to_include_players_class_instantiation():
    all_players = Players(6)
    card_dealer = CardDealer(6)
    game_round = GameRound(all_players, card_dealer)
    assert type(game_round.players_information.player1.money) is int


class TestGameRoundPayingBlinds(unittest.TestCase):

    def setUp(self):
        n_players = 3
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.starting_player_money = 100
        self.starting_player_amount_bet = 0
        self.game_round.big_blind = 20
        self.game_round.small_blind = 10

    def test_big_blind_player_correctly_assigned(self):
        self.assertEqual(self.game_round.big_blind_player, 'player3')

    def test_small_blind_player_correctly_assigned(self):
        self.assertEqual(self.game_round.small_blind_player, 'player2')

    def test_pay_big_blind(self):
        self.assertEqual(
            self.game_round.players_information.player3.money,
            self.starting_player_money
        )
        self.game_round.pay_blinds()
        self.assertEqual(
            self.game_round.players_information.player3.money,
            self.starting_player_money - self.game_round.big_blind
        )
        self.assertEqual(
            self.game_round.players_information.player3.amount_bet_in_round,
            self.starting_player_amount_bet + self.game_round.big_blind
        )

    def test_pay_small_blind(self):

        self.assertEqual(
            self.game_round.players_information.player2.money,
            self.starting_player_money
        )
        self.game_round.pay_blinds()
        self.assertEqual(
            self.game_round.players_information.player2.money,
            self.starting_player_money - self.game_round.small_blind
        )
        self.assertEqual(
            self.game_round.players_information.player2.amount_bet_in_round,
            self.starting_player_amount_bet + self.game_round.small_blind
        )

    def test_paying_blinds_adds_to_pot(self):
        self.assertNotEqual(
            self.game_round.pot,
            self.game_round.big_blind + self.game_round.small_blind
        )
        self.game_round.pay_blinds()
        self.assertEqual(
            self.game_round.pot,
            self.game_round.big_blind + self.game_round.small_blind
        )

    def test_paying_blinds_adds_to_record_of_highest_round_bet(self):
        self.assertNotEqual(
            self.game_round.highest_round_bet,
            self.game_round.big_blind)
        self.game_round.pay_blinds()
        self.assertEqual(
            self.game_round.highest_round_bet,
            self.game_round.big_blind
        )


class TestGameRoundPlayingOrder(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.starting_player_money = 100
        self.starting_player_amount_bet = 0
        self.game_round.big_blind = 20
        self.game_round.small_blind = 10

    def test_pre_flop_playing_order_and_blind_and_dealer_positions(self):
        self.assertEqual(
            self.game_round.pre_flop_playing_order[-1],
            self.game_round.big_blind_player
        )
        self.assertEqual(
            self.game_round.pre_flop_playing_order[-2],
            self.game_round.small_blind_player
        )
        self.assertEqual(
            self.game_round.pre_flop_playing_order[-3],
            self.game_round.dealer_player
        )

    def test_post_flop_playing_order_and_blinds_and_dealer_positions(self):
        self.assertEqual(
            self.game_round.post_flop_playing_order[1],
            self.game_round.big_blind_player
        )
        self.assertEqual(
            self.game_round.post_flop_playing_order[0],
            self.game_round.small_blind_player
        )
        self.assertEqual(
            self.game_round.post_flop_playing_order[-1],
            self.game_round.dealer_player
        )


class TestPlayerActions(unittest.TestCase):
    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.starting_player_money = 100
        self.starting_player_amount_bet = 0
        self.game_round.big_blind = 20
        self.game_round.small_blind = 10

    def test_call_big_blind_successful(self):
        self.game_round.pay_blinds()
        start_money = self.game_round.players_information.player3.money
        self.game_round.call_bet('player3')
        post_call_money = self.game_round.players_information.player3.money
        self.assertLess(post_call_money, start_money)
        self.assertEqual(
            start_money - post_call_money,
            self.game_round.big_blind
        )

    def test_call_bet_unsuccessful(self):
        self.game_round.players_information.__dict__['player1'].money = 50
        self.game_round.highest_round_bet = 100
        self.assertFalse(self.game_round.call_bet('player1'))


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


def test_is_player_required_to_act():
    n_players = 7
    game_round = GameRound(Players(n_players), CardDealer(n_players))
    player_1 = game_round.players_information.player1
    game_round.highest_round_bet = 100
    player_1.amount_bet_in_round = 50
    assert game_round.is_player_required_to_act(player_1) is True
    game_round.highest_round_bet = 0
    game_round.players_information.player1.amount_bet_in_round = 0
    assert game_round.is_player_required_to_act(player_1) is True
    game_round.highest_round_bet = 100
    player_1.amount_bet_in_round = 100
    assert game_round.is_player_required_to_act(player_1) is False




class TestBetting(unittest.TestCase):
    n_players = 3
    game_round = GameRound(Players(n_players), CardDealer(n_players))
    player1 = game_round.players_information.player1
    player2 = game_round.players_information.player2
    player3 = game_round.players_information.player3
    all_players: dict = game_round.players_information.__dict__

    def test_clear_player_bets_at_round_end(self):
        self.player1.amount_bet_in_round = 100
        self.game_round.clear_player_bets_at_round_end()
        self.assertEqual(self.player1.amount_bet_in_round, 0)

    def test_each_player_has_matched_highest_bet(self):
        self.game_round.highest_round_bet = 75
        self.player1.amount_bet_in_round = 75
        self.player2.amount_bet_in_round = 75
        self.player3.amount_bet_in_round = 75
        self.assertTrue(
            self.game_round.each_player_matched_highest_bet(self.all_players)
        )
        self.player3.amount_bet_in_round = 70
        self.assertFalse(
            self.game_round.each_player_matched_highest_bet(self.all_players)
        )




if __name__ == '__main__':
    unittest.main()









