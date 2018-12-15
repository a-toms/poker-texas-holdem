from hand_of_cards import (
    Card, Player, Players, CardDealer, HandRanker,
    HandClassifier, GameRound, Hand
)
import unittest
from unittest.mock import patch


class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = Card(14, 'D')

    def test_card_creation(self):
        self.assertEqual(Card, type(self.card))

    def test_card_rank(self):
        self.assertEqual(
            14,
            self.card.rank
        )

    def test_card_suit(self):
        self.assertEqual(
            'D',
            self.card.suit
        )

    def test_card_representation(self):
        self.assertEqual(
            str(self.card.__str__()),  # This only passes if converted to a str. Why?
            "Ace of Diamonds"
        )


class TestDealingCards(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.card_dealer = CardDealer(n_players)
        self.all_players = Players(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.suites = ('H', 'C', 'S', 'D')
        self.numbers = [i for i in range(2, 15)]

    def test_52_cards_in_deck(self):
        self.assertIs(52, len(self.card_dealer.deck))

    def test_pick_card(self):
        card = self.card_dealer.pick_card()
        self.assertIn(card.rank, self.numbers)
        self.assertIn(card.suit, self.suites)

    def test_deal_pocket_cards_to_players_two_cards(self):
        self.assertTrue(self.all_players.player1.hand.pocket_cards == [])
        self.game_round.card_dealer.deal_pocket_cards(self.all_players)
        self.assertEqual(
            2,
            len(self.all_players.player1.hand.pocket_cards)
        )
        self.assertEqual(
            2,
            len(self.all_players.player2.hand.pocket_cards)
        )

    def test_deal_pocket_cards_to_players_dealt_card(self):
        self.card_dealer.deal_pocket_cards(self.all_players)
        self.assertEqual(
            str,
            type(self.all_players.player1.hand.pocket_cards[0].suit)
            )
        self.assertEqual(
            int,
            type(self.all_players.player1.hand.pocket_cards[0].rank)
        )
        self.assertEqual(
            type(self.all_players.player1.hand.pocket_cards[0]),
            Card
        )

    def test_deal_pocket_cards_to_players_dealt_two_cards(self):
        self.card_dealer.deal_pocket_cards(self.all_players)
        self.assertEqual(
            len(self.all_players.player1.hand.pocket_cards),
            2
        )


class TestPlayerHandCreation(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.card_dealer = CardDealer(n_players)
        self.all_players = Players(n_players)

    def test_player_creates_hand_object(self):
        self.assertEqual(
            type(self.all_players.player1.hand),
            Hand
        )

    def test_dealer_deals_two_objects_to_player_hand(self):
        self.card_dealer.deal_pocket_cards(self.all_players)
        self.assertEqual(
            len(self.all_players.player1.hand.pocket_cards),
            2
        )

    def test_dealer_deals_cards_to_player_hand(self):
        self.card_dealer.deal_pocket_cards(self.all_players)
        hand = self.all_players.player1.hand
        self.assertEqual(
            type(hand.pocket_cards[0]),
            Card
        )
        self.assertEqual(
            type(hand.pocket_cards[1]),
            Card
        )


class TestPlayerHandRanking(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.card_dealer = CardDealer(n_players)
        self.all_players = Players(n_players)
        self.card_dealer.table_cards = [
            Card(3, "H"), Card(2, "H"), Card(6, "H"),
            Card(10, "H"), Card(10, "D")
        ]
        self.all_players.player1.hand.pocket_cards = [
            Card(10, 'S'), Card(8, 'C')
        ]
        self.player_1_hand = self.all_players.player1.hand


    def test_generate_possible_combinations(self):
        """
        There are 21 combinations when taking a sample of 5 from 7 objects.
        """
        self.assertEqual(
            21,
            len(list(self.player_1_hand.generate_hand_combinations(
                    self.card_dealer)))
        )

    def test_get_highest_hand_score_from_combinations(self):
        possible_combinations = self.player_1_hand.generate_hand_combinations(
            self.card_dealer
        )
        three_of_a_kind_rank = 4
        self.assertEqual(
            three_of_a_kind_rank,
            self.player_1_hand.get_highest_hand_score(possible_combinations)
        )

    def test_filter_for_hands_with_highest_rank(self):
        # Itertools object appears to be depleted when called! Yes! Note this.
        sample_combinations = list(self.player_1_hand.generate_hand_combinations(
            self.card_dealer)
        )
        highest_score_hands_in_sample = 6
        self.assertEqual(
            highest_score_hands_in_sample,
            len(self.player_1_hand.filter_hands_by_highest_score(
                sample_combinations))
        )

    def test_get_card_ranks(self):
        self.assertListEqual(
            [10, 10, 6, 3, 2],
            self.player_1_hand.get_card_ranks(self.card_dealer.table_cards)
        )

    def test_get_hand_with_highest_card_rank_same_pair(self):
        test_hand_1 = [
            Card(10, "H"), Card(6, "D"), Card(6, "H"),
            Card(9, "H"), Card(2, "C")
        ]
        test_hand_2 = [
            Card(14, "C"), Card(6, "D"), Card(6, "H"),
            Card(3, "H"), Card(2, "H")
        ]
        test_input = [test_hand_1, test_hand_2]
        # test_hand_2 is the higher hand
        self.assertEqual(
            self.player_1_hand.get_hand_with_highest_card_rank(test_input),
            test_hand_2
        )

    def test_get_hand_with_highest_card_rank_different_pair(self):
        test_hand_1 = [
            Card(10, "H"), Card(2, "D"), Card(2, "H"),
            Card(9, "H"), Card(6, "C")
        ]
        test_hand_2 = [
            Card(3, "H"), Card(6, "D"), Card(6, "H"),
            Card(2, "H"), Card(14, "C")
        ]
        test_input = [test_hand_1, test_hand_2]
        # test_hand_2 is the higher hand
        self.assertEqual(
            self.player_1_hand.get_hand_with_highest_card_rank(test_input),
            test_hand_2
        )
        # I do not

    def test_calculate_best_hand(self):
        self.player_1_hand.pocket_cards = [Card(6, 'D'), Card(6, 'H')]
        self.card_dealer.table_cards = [
            Card(6, 'S'), Card(12, 'H'), Card(12, 'D'), Card(12, 'S'),
            Card(14, 'D')
        ]
        # The best hand from player1's pocket cards and the table cards is
        # a full house with three 12s and two 6s
        suit_and_rank = [
            x.return_rank_and_suit()
            for x in self.player_1_hand.calculate_best_hand(self.card_dealer)
        ]
        self.assertCountEqual(
            [(12, 'H'), (12, 'D'), (12, 'S'),
             (6, 'D'), (6, 'H')],
            suit_and_rank
        )

    def tearDown(self):
        self.card_dealer.table_cards = []



class TestHandRankingSystem(unittest.TestCase):
    def setUp(self):
        self.ranker = HandRanker()

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
        straight_flush_cards = self.ranker.get_straight_flush(ExampleHands.test_straight_flush)
        rank_and_suit_of_cards = [
            card.return_rank_and_suit() for card in straight_flush_cards
        ]
        self.assertEqual(
            [(1, 'C'), (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C')],
            rank_and_suit_of_cards,
        )

    def test_no_straight_flush(self):
        self.assertIsNone(
            self.ranker.get_straight_flush(ExampleHands.test_no_straight_flush)
        )


class ExampleHands:

    test_high_card = [
        Card(1, 'C'), Card(2, 'C'), Card(4, 'S'),
        Card(3, 'S'), Card(7, 'D')
    ]

    test_pair = [
        Card(1, 'C'), Card(2, 'C'), Card(4, 'S'),
        Card(3, 'S'), Card(4, 'D')
    ]
    test_no_pair = [
        Card(1, 'C'), Card(10, 'C'), Card(4, 'S'),
        Card(3, 'S'), Card(9, 'D')
    ]
    test_two_pairs = [
        Card(1, 'C'), Card(2, 'C'), Card(4, 'S'),
        Card(2, 'S'), Card(4, 'D')
    ]
    test_no_two_pairs = [
        Card(2, 'C'), Card(10, 'C'), Card(4, 'S'),
        Card(3, 'S'), Card(4, 'D')
    ]
    test_no_triples = [
        Card(10, 'C'), Card(2, 'C'), Card(10, 'S'),
        Card(3, 'S'), Card(9, 'D')
    ]
    test_triples = [
        Card(10, 'C'), Card(2, 'C'), Card(10, 'S'),
        Card(3, 'S'), Card(10, 'D')
    ]
    test_straight = [
        Card(5, 'C'), Card(3, 'D'), Card(2, 'S'),
        Card(4, 'H'), Card(1, 'D')
    ]
    test_no_straight = [
        Card(10, 'C'), Card(7, 'C'), Card(10, 'S'),
        Card(9, 'H'), Card(1, 'D')
    ]
    test_no_straight2 = [
        Card(5, 'C'), Card(3, 'D'), Card(3, 'S'),
        Card(4, 'H'), Card(1, 'D')
    ]
    test_ace_high_straight = [
        Card(14, 'C'), Card(11, 'D'), Card(12, 'S'),
        Card(10, 'H'), Card(13, 'D')
    ]
    test_no_ace_high_straight = [
        Card(10, 'C'), Card(13, 'C'), Card(12, 'S'),
        Card(11, 'H'), Card(1, 'D')
    ]
    test_flush = [
        Card(10, 'C'), Card(2, 'C'), Card(5, 'C'),
        Card(3, 'C'), Card(1, 'C')
    ]
    test_no_flush = [
        Card(10, 'C'), Card(4, 'C'), Card(10, 'S'),
        Card(8, 'C'), Card(3, 'C')
    ]
    test_full_house = [
        Card(10, 'C'), Card(10, 'D'), Card(10, 'S'),
        Card(8, 'H'), Card(8, 'D')
    ]
    test_no_full_house = [
        Card(10, 'C'), Card(2, 'C'), Card(10, 'S'),
        Card(10, 'H'), Card(1, 'D')
    ]
    test_no_quads = [
        Card(10, 'C'), Card(2, 'C'), Card(10, 'S'),
        Card(8, 'H'), Card(10, 'D')
    ]
    test_quads = [
        Card(10, 'C'), Card(2, 'C'), Card(10, 'S'),
        Card(10, 'H'), Card(10, 'D')
    ]
    test_straight_flush = [
        Card(1, 'C'), Card(2, 'C'), Card(5, 'C'),
        Card(3, 'C'), Card(4, 'C')
    ]
    test_no_straight_flush = [
        Card(10, 'C'), Card(2, 'C'), Card(5, 'C'),
        Card(3, 'C'), Card(1, 'C')
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
        (2, [(12, 'H'), (12, 'C'), (6, 'S'), (7, 'C'), (8, 'H')]),  # 2D, 3H
        (2, [(12, 'H'), (12, 'C'), (10, 'D'), (9, 'D'), (8, 'H')]),  # 10D, 9D
        (7, [(12, 'H'), (12, 'C'), (12, 'D'), (8, 'C'), (8, 'H')]),  # 12D , 8C
        (7, [(12, 'H'), (12, 'C'), (12, 'S'), (7, 'C'), (7, 'S')])  # 12S, 7S
    ]


class TestHandRanker(unittest.TestCase):
    """
    Check that rank numbers are correctly output for each hand.
    """
    def setUp(self):
        self.hand_classifier = HandRanker()
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

    def test_check_straight_flush(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_straight_flush),
            self.hand_and_rank['straight flush']
        )

    def test_check_quads(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_quads),
            self.hand_and_rank['four of a kind']
        )

    def test_check_full_house(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_full_house),
            self.hand_and_rank['full house']
        )

    def test_check_flush_classifier(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_flush),
            self.hand_and_rank['flush']
        )

    def test_check_straight(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_straight),
            self.hand_and_rank['straight']
        )

    def test_check_triples(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_triples),
            self.hand_and_rank['three of a kind']
        )

    def test_check_two_pairs(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_two_pairs),
            self.hand_and_rank['two pairs']
        )

    def test_check_pair(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_pair),
            self.hand_and_rank['pair']
        )

    def test_check_high_card(self):
        self.assertEqual(
            self.hand_classifier.rank_hand(ExampleHands.test_high_card),
            self.hand_and_rank['high card']
        )

    def test_check_all_hands(self):
        self.assertEqual(
            self.hand_classifier.rank_hands(ExampleHands().sample_hands),
            ExampleHands().all_ranked_hands
        )


class TestHandClassifier(unittest.TestCase):

    def setUp(self):
        self.find_best_hand = HandClassifier()

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

    def test_get_card_numbers_from_cards_in_highest_rank(self):
        """
        3H, 3C, 4S, 14C and 8H on the board. 5 players.
        The test_hand is ranked.
        """
        test_hand = [
            (3, [Card(2, 'H'), Card(2, 'C'), Card(3, 'H'), Card(14, 'C'),
                 Card(3, 'C')]),  # pocket cards = 2C 2H
            (2, [Card(3, 'H'), Card(3, 'C'), Card(6, 'H'), Card(14, 'C'),
                 Card(8, 'H')]),  # pocket cards = 2D, 6H
            (3, [Card(3, 'H'), Card(4, 'D'), Card(4, 'S'), Card(14, 'C'),
                 Card(14, 'D')]),  # pocket cards = 14D, 4D
            (3, [Card(3, 'H'), Card(3, 'C'), Card(8, 'C'), Card(14, 'C'),
                 Card(8, 'H')]),  # pocket cards = 12D , 8C
            (2, [Card(3, 'H'), Card(3, 'C'), Card(12, 'S'), Card(14, 'C'),
                 Card(8, 'H')])  # pocket cards = 12S, 7S
        ]
        self.assertEqual(
            self.find_best_hand.get_card_numbers_from_cards_in_highest_rank(test_hand),
            [[3, 3, 2, 2, 14], [14, 14, 4, 4, 3], [8, 8, 3, 3, 14]]
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


class TestGameRoundClassInstantiation(unittest.TestCase):
    def test_game_round_instantiates_to_include_player_class_instantiation(self):
        n_players = 6
        all_players = Players(n_players)
        card_dealer = CardDealer(n_players)
        game_round = GameRound(all_players, card_dealer)
        self.assertEqual(
            Player,
            type(game_round.players_information.player1)
        )


class TestPlayerPaymentsAfterAllIn(unittest.TestCase):
    def setUp(self):
        self.n_players = 8
        self.all_players = Players(self.n_players)
        self.card_dealer = CardDealer(self.n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)


    def test_get_any_player_that_is_all_in(self):
        # no player is all_in
        self.assertEqual(
            (),
            tuple(self.all_players.get_any_player_that_is_all_in())
        )

        # player8 is all_in
        self.all_players.player8.is_all_in = True
        self.assertEqual(
            self.all_players.player8,
            tuple(self.all_players.get_any_player_that_is_all_in())[0]
        )

    def test_set_max_winnings(self):
        """
        This tests that an all_in player's max winnings are capped after
        he goes all_in at his highest bet * number of players.
        """
        # Assign bets to players.
        for player in self.all_players.__dict__.values():
            player.amount_bet_in_round = 20

        # Assign larger bets to some players.
        self.all_players.player1.amount_bet_in_round = 40
        self.all_players.player2.amount_bet_in_round = 40
        player3 = self.all_players.player3
        player3.amount_bet_in_round = 30

        sum_of_bets_for_each_player_equal_or_less_than_all_in_players_bet = 190

        # player3 is the only all_in player.
        player3.is_all_in = True

        self.assertEqual(
            0,
            player3.max_winnings
        )
        self.all_players.set_max_winnings(player3)
        self.assertEqual(
            sum_of_bets_for_each_player_equal_or_less_than_all_in_players_bet,
            player3.max_winnings
        )



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
        self.assertEqual(self.game_round.big_blind_player.name, 'player3')
        self.assertTrue(
            self.game_round.players_information.player3.in_big_blind_position)

    def test_small_blind_player_correctly_assigned(self):
        self.assertEqual(self.game_round.small_blind_player.name, 'player2')

    def test_pay_big_blind(self):
        self.assertEqual(
            self.game_round.players_information.player3.money,
            self.starting_player_money
        )
        self.game_round.pay_blinds()
        self.assertEqual(
            self.game_round.players_information.player3.money,
            (self.starting_player_money - self.game_round.big_blind)
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


class TestEndOfRoundActions(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.game_round.players_information.player1.money = 100

    def test_give_pot_to_winners(self):
        self.game_round.pot = 500
        winners = ('player1', 'player2')
        self.assertEqual(
            self.game_round.players_information.player1.money,
            100
        )
        self.game_round.give_pot_to_winners(winners)
        self.assertEqual(
            self.game_round.players_information.player1.money,
            350
        )
        self.assertTrue(self.game_round.pot == 0)


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

    def test_playing_order_and_blind_and_dealer_positions(self):
        self.assertEqual(
            self.game_round.playing_order[-1],
            self.game_round.big_blind_player
        )
        self.assertEqual(
            self.game_round.playing_order[-2],
            self.game_round.small_blind_player
        )
        self.assertEqual(
            self.game_round.playing_order[-3],
            self.game_round.dealer_player
        )

    def test_playing_order_big_blind_position(self):
        self.assertEqual(
            self.game_round.playing_order[-1],
            self.game_round.big_blind_player
        )

    def test_playing_order_small_blind_player_position(self):
        self.assertEqual(
            self.game_round.playing_order[-2],
            self.game_round.small_blind_player
        )

    def test_playing_order_dealer_player_position(self):
        self.assertEqual(
            self.game_round.playing_order[-3],
            self.game_round.dealer_player
        )

    def test_player_pre_flop_position(self):
        """
        With 8 players, player 7 is in the big blind position so penultimate to act pre-flop.
        """
        self.assertEqual(
            self.game_round.players_information.player7,
            self.game_round.playing_order[-2]
        )

    def test_player_post_flop_position(self):
        """
        With 8 players, player 7 is first to act after the flop.
        """
        self.game_round.rotate_playing_order_before_flop()
        self.assertEqual(
            self.game_round.players_information.player7,
            self.game_round.playing_order[0]
        )


class TestPlayerActions(unittest.TestCase):
    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.player1 = self.game_round.players_information.player1
        self.game_round.big_blind = 20
        self.game_round.small_blind = 10

    def test_call_big_blind_successful(self):
        self.game_round.pay_blinds()
        start_money = self.player1.money
        self.game_round.call_bet(self.player1)
        post_call_money = self.player1.money
        self.assertLess(post_call_money, start_money)
        self.assertEqual(
            start_money - post_call_money,
            self.game_round.big_blind
        )

    def test_call_bet_unsuccessful(self):
        self.player1.money = 40
        self.player1.amount_bet_in_round = 0
        self.game_round.highest_round_bet = 100
        self.assertFalse(self.game_round.call_bet(self.player1))


class TestFoldHand(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.starting_player_amount_bet = 0
        self.game_round.big_blind = 20
        self.game_round.small_blind = 10
        self.player1 = self.game_round.players_information.player1

    def test_fold(self):
        self.assertFalse(self.player1.has_folded_hand)
        self.game_round.fold_hand(self.player1)
        self.assertTrue(self.player1.has_folded_hand)


class TestPlayerHasRemainingActions(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.all_players = Players(n_players)
        self.card_dealer = CardDealer(n_players)
        self.game_round = GameRound(self.all_players, self.card_dealer)
        self.player1 = self.game_round.players_information.player1

    def test_has_remaining_actions_not_yet_bet_enough(self):
        self.game_round.highest_round_bet = 50
        self.player1.amount_bet_in_round = 45
        self.assertTrue(self.game_round.has_remaining_actions(self.player1))

    def test_has_remaining_actions_player_not_yet_made_action(self):
        """
        This tests that function shows that the player has remaining actions if
        a) the player's amount bet matches the highest round bet, and b) the
        player has not acted in round. Example of occurrence is if the player is
        big blind and all other players merely called the big blind or folded,
        with no raises.
        """
        self.game_round.highest_round_bet = 50
        self.player1.amount_bet_in_round = 50
        self.player1.has_acted_in_round = False
        self.assertTrue(self.game_round.has_remaining_actions(self.player1))

    def test_has_remaining_actions_folded_hand(self):
        self.player1.has_folded_hand = True
        self.assertFalse(self.game_round.has_remaining_actions(self.player1))

    def test_has_remaining_actions_player_has_acted_and_matched_bet(self):
        """
        This tests that function shows that player has no remaining actions or
        after player has acted in the round, matched the highest bet, and not
        folded.
        """
        self.game_round.highest_round_bet = 50
        self.player1.amount_bet_in_round = 50
        self.player1.has_folded_hand = False
        self.player1.has_acted_in_round = True
        self.assertFalse(self.game_round.has_remaining_actions(self.player1))

    def test_at_least_one_player_has_remaining_action(self):
        self.all_players.player4.has_acted_in_round = False
        self.assertTrue(
            self.game_round.at_least_one_player_has_remaining_action
        )


class TestPlayerInput(unittest.TestCase):
    # Perhaps unnecessary. One need not test IO.

    @patch('builtins.input', lambda: 'y')
    def test_input_mocking(self):
        self.assertEqual(input(), 'y')


class TestBetting(unittest.TestCase):
    n_players = 3
    game_round = GameRound(Players(n_players), CardDealer(n_players))
    player1 = game_round.players_information.player1

    def test_reset_players_status_at_round_end_reset_amount_bet_in_round(self):
        self.player1.amount_bet_in_round = 100
        self.game_round.reset_players_status_at_round_end()
        self.assertEqual(0, self.player1.amount_bet_in_round)

    def test_reset_players_status_at_round_end_reset_has_acted_marker(self):
        self.player1.has_acted_in_round = True
        self.game_round.reset_players_status_at_round_end()
        self.assertFalse(self.player1.has_acted_in_round)

    def test_reset_highest_round_bet(self):
        self.game_round.highest_round_bet = 100
        self.game_round.reset_highest_round_bet()
        self.assertEqual(
            0,
            self.game_round.highest_round_bet
        )


class TestBoardDealing(unittest.TestCase):

    def setUp(self):
        n_players = 8
        self.game_round = GameRound(Players(n_players), CardDealer(n_players))
        self.rank = tuple(range(2, 15))
        self.suit = ('H', 'D', 'S', 'C')

    def test_deal_board_flop_deal_three(self):
        self.assertEqual([], self.game_round.card_dealer.table_cards)
        self.game_round.card_dealer.deal_flop()
        self.assertEqual(
            3,
            len(self.game_round.card_dealer.table_cards)
        )

    def test_deal_board_flop_deal_card(self):
        self.assertEqual(self.game_round.card_dealer.table_cards, [])
        self.game_round.card_dealer.deal_flop()
        self.assertTrue(
            self.game_round.card_dealer.table_cards[0].rank in self.rank
        )
        self.assertTrue(
            self.game_round.card_dealer.table_cards[0].suit in self.suit
        )

    def test_deal_card_to_table_deals_card(self):
        self.assertEqual(self.game_round.card_dealer.table_cards, [])
        self.game_round.card_dealer.deal_card_to_table()
        self.assertTrue(
            self.game_round.card_dealer.table_cards[0].rank in self.rank
        )
        self.assertTrue(
            self.game_round.card_dealer.table_cards[0].suit in self.suit
        )
        self.assertEqual(
            1,
            len(self.game_round.card_dealer.table_cards)
        )

    def tearDown(self):
        del self.game_round.card_dealer.table_cards[:]


if __name__ == '__main__':
    unittest.main()
