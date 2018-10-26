import itertools
from collections import deque
import copy
import random
import logging
logging.basicConfig(level=logging.INFO)


class Player:
    money = 100
    amount_bet_in_round = 0

    def __init__(self, name):
        self.name = name


class Players(Player):
    """Use __dict__ to access the different players in Players."""
    def __init__(self, number_of_players):
        for i in range(1, number_of_players + 1):
            setattr(self, f'player{i}', Player(f'player{i}'))


class CardDealer:
    dealt_cards = []
    deck = list(itertools.product(range(2, 15), ('H', 'D', 'S', 'C')))
    pocket_cards = {}

    def __init__(self, n_of_players, n_of_pocket_cards):
        self.number_of_players = n_of_players
        self.number_of_pocket_cards = n_of_pocket_cards

    def pick_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        self.dealt_cards.append(card)
        return card

    def deal_pocket_cards(self):
        for i in range(1, self.number_of_players + 1):
            self.pocket_cards[f'player{i}'] = [
                self.pick_card() for _ in self.number_of_pocket_cards
            ]


class GetHandRanks:

    def get_high_card(self, hand):
        card_numbers = tuple(set([card[0] for card in hand]))
        return tuple(sorted(card_numbers))

    def get_pairs(self, hand):
        card_numbers = [card[0] for card in hand]
        number_of_cards_in_a_pair = 2
        pairs = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == number_of_cards_in_a_pair:
                pairs += (card_number,)
        if pairs != ():
            return tuple(set(pairs))

    def get_two_pairs(self, hand):
        try:
            if len(set(self.get_pairs(hand))) == 2:
                return set(self.get_pairs(hand))
        except TypeError:  # This excepts where hand is None because no pair
            pass

    def get_three_of_a_kind(self, hand):
        card_numbers = [card[0] for card in hand]
        triples = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 3:
                triples += (card_number,)
        if triples != ():
            return triples

    def get_straight_with_low_ace(self, hand):
        """Check if a straight exists if the ace is treated as a low ace."""
        low_ace, high_ace = 1, 14
        card_numbers = set([card[0] for card in hand])
        card_numbers = [low_ace if n == high_ace else n for n in card_numbers]
        card_numbers.sort()
        high_card, low_card = card_numbers[-1], card_numbers[0]
        if len(card_numbers) == 5 and high_card - low_card == 4:
            return tuple(card_numbers)

    def get_straight_without_low_ace(self, hand):
        card_numbers = list(set(sorted([card[0] for card in hand])))
        high_card, low_card = card_numbers[-1], card_numbers[0]
        if len(card_numbers) == 5 and high_card - low_card == 4:
            return tuple(card_numbers)

    def get_straights(self, hand):
        straight_functions = (
            self.get_straight_with_low_ace,
            self.get_straight_without_low_ace
        )
        for f in straight_functions:
            if f(hand):
                return f(hand)

    def get_flush(self, hand):
        card_suites = tuple([card[1] for card in hand])
        card_numbers = [card[0] for card in hand]
        if len(card_numbers) == 5 and len(set(card_suites)) == 1:
            return card_suites[1]

    def get_full_house(self, hand):
        card_numbers = tuple([card[0] for card in hand])
        if self.get_three_of_a_kind(hand) is not None:
            if self.get_pairs(hand):
                return tuple(card_numbers)

    def get_four_of_a_kind(self, hand):
        card_numbers = [card[0] for card in hand]
        quads = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 4:
                quads += (card_number,)
        if quads != ():
            return quads

    def get_straight_flush(self, hand):
        if self.get_straights(hand) and self.get_flush(hand):
            return sorted(hand)


class ClassifyHand(GetHandRanks):

    ranked_hands = []
    hand_ranks = {
        GetHandRanks.get_straight_flush: 9,
        GetHandRanks.get_four_of_a_kind: 8,
        GetHandRanks.get_full_house: 7,
        GetHandRanks.get_flush: 6,
        GetHandRanks.get_straights: 5,
        GetHandRanks.get_three_of_a_kind: 4,
        GetHandRanks.get_two_pairs: 3,
        GetHandRanks.get_pairs: 2,
        GetHandRanks.get_high_card: 1
    }

    def rank_hand(self, hand):
        for f, rank in self.hand_ranks.items():
            if f(self, hand):
                return rank

    def rank_hands(self, hands):
        """Get each hand and assign it a rank."""
        ranked_hands = []
        for hand in hands:
            rank = self.rank_hand(sorted(hand))
            ranked_hands.append((rank, hand))
        return ranked_hands


class FindBestHand:
    def get_highest_rank(self, ranked_hands):
        """Find the highest rank from several hands."""
        highest_rank = 0
        for ranked_hand in ranked_hands:
            if ranked_hand[0] > highest_rank:
                highest_rank = ranked_hand[0]
        return highest_rank

    def get_card_numbers_from_highest_ranked_cards(self, ranked_hands):
        """Return card numbers from only the hands with the highest rank."""
        highest_rank = self.get_highest_rank(ranked_hands)
        hands_with_highest_rank = []
        for ranked_hand in ranked_hands:
            if ranked_hand[0] == highest_rank:
                hands_with_highest_rank.append(
                    self.get_card_numbers_from_ranked_hand(ranked_hand))
        return hands_with_highest_rank

    def get_card_numbers_from_ranked_hand(self, ranked_hand):
        """Convert a ranked hand to the hand's card numbers."""
        card_numbers = [card[0] for card in ranked_hand[1]]
        card_numbers = self.sort_by_frequency_and_size(card_numbers)
        return card_numbers

    def sort_by_frequency_and_size(self, card_numbers):
        card_numbers.sort(reverse=True)  # Descending card number size
        card_numbers = sorted(
            card_numbers, key=lambda n: card_numbers.count(n), reverse=True)  # Descending card number frequency
        return card_numbers

    def get_highest_card(self, card_numbers):
        card_numbers = list(set(card_numbers))
        return self.sort_by_frequency_and_size(card_numbers)[0]

    def get_winner_from_ranked_hands(self, ranked_hands):
        card_numbers = self.get_card_numbers_from_highest_ranked_cards(
            ranked_hands)
        best_hand = self.get_highest_card(card_numbers)
        return best_hand


class GameRound:
    # self.players_information.player1 -> instantiation of Players(Player)
    """Player order represents the players' different positions in relation to
    the dealer around the table. The initial pre-flop positions are rotated
    after the pre-flop round."""

    highest_round_bet = 0
    pot = 0
    small_blind = 20
    big_blind = 40

    def __init__(self, instantiated_players_class):
        self.players_information = instantiated_players_class
        self.player_position_order = deque(
            [player for player in self.players_information.__dict__.keys()]
        )
        self.pre_flop_playing_order = copy.deepcopy(self.player_position_order)
        self.post_flop_playing_order = self.get_post_flop_playing_order()
        self.small_blind_player = self.pre_flop_playing_order[-2]
        self.big_blind_player = self.pre_flop_playing_order[-1]
        self.dealer_player = self.pre_flop_playing_order[-3]

    def get_post_flop_playing_order(self):
        post_flop_playing_order = copy.deepcopy(self.player_position_order)
        post_flop_playing_order.rotate(2)
        return post_flop_playing_order

    def pay_blinds(self):
        self.players_information.__dict__[self.small_blind_player].money -= self.small_blind
        self.players_information.__dict__[self.big_blind_player].money -= self.big_blind
        self.pot += self.big_blind + self.small_blind
        self.highest_round_bet = self.big_blind

    def call_bet(self, player):
        call_amount = (
                self.highest_round_bet -
                self.players_information.__dict__[player].amount_bet_in_round
        )
        self.players_information.__dict__[player].money -= call_amount
        self.pot += call_amount

    def fold_hand(self, player):
        self.pre_flop_playing_order.remove(player)
        self.post_flop_playing_order.remove(player)

    def raise_bet(self, player, bet_size):
        raising_player = self.players_information.__dict__[player]
        if raising_player.money - bet_size < 0:
            print(f"Invalid bet. {player} does not have enough money.")
            return False
        raising_player.money -= bet_size
        raising_player.amount_bet_in_round += bet_size
        self.highest_round_bet = raising_player.amount_bet_in_round
        self.pot += bet_size

    def check(self, player): # Todo - Continue by writing tests here
        checking_player = self.players_information.__dict__[player].amount_bet_in_round
        if checking_player.amount_bet_in_round == self.highest_round_bet:
            return True
        else:
            print(f"Invalid bet. {player} must match the highest current bet "+
                  f"of {self.highest_round_bet} to check")
            return False

    def ask_player_for_actions(self, player):
        actions = {
            1: self.check, 2: self.call_bet, 3: self.raise_bet,
            4: self.fold_hand
        }
        action = self.get_player_action(player)
        # Work on this section. How do I access a func from a dict and call arguments
        actions[action](player, *kwargs)

    def get_player_action(self, player):
        return int(input(
            f"{player},\n" +
            "the highest bet of the round so far is {highest_round_bet}." +
            f"You have {player.money} currently." +
            f"You have bet {player.amount_bet} this round." +
            "Would you like to check (1), call (2), raise (3), or fold (4) ?" +
            "Enter action: "))

    def clear_bets_for_each_player_at_end_of_game_round(self):
        #Wipe each players record of game round betting
        pass

    def adjust_player_order_for_next_round(self):
        pass

def main():
    all_players = Players(5)
    dealer = CardDealer(5, 2)
    dealer.deal_pocket_cards()
    print(dealer.pocket_cards)


""" Will require a method to match the highest card numbers to the particular
player. I like that the current methods will find the best hand in a 
player-neutral manner. The player-hand-matching method should be discrete"""


if __name__ == "__main__":
    main()


"""Game mechanics:

    1. Represent the board and pocket cards
    Have a board representation that the player can access, e.g.,
    board = [(3, 'H'), (3, 'C'), (4, 'S'), (14, 'C'), (8, 'H')], and
    deal pocket cards to each player, e.g.,
    hand = [(3, 'S'), (3, 'D').

    2. Find the best hand that the player can form. 

    Do this by running get_hand_rank for each permutation*1 that the player can 
    form with his pocket cards. Note that the player may be able to form 
    multiple top ranking hands using 1 of his pocket cards. For example, if he
    has (4, 'D'), (3,'D') and the board cards are all 'D', he could form a 
    flush with either card. The highest flush that he can make may involve him
    using 1, 2, or none of his pocket cards. 

    Accordingly, find the best hand that the player can form by:
        - ranking all the hands that he can form using the hand_ranking func
        - finding the best hand from the hands that he can form. If there is a 
          tie in the best hands that he can form, pick one of them arbitrarily.

    I note that finding the individual's best hand is very similar to finding 
    the best hand among multiple players.

    *1 Use itertools.permutations


    """
