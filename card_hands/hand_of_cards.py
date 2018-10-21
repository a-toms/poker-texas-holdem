import itertools
import random
import logging
logging.basicConfig(level=logging.INFO)
from collections import deque


class Player:
    money = 100

    def __init__(self, name):
        self.name = name


class Players(Player):
    """Use __dict__ to access the different players in Players"""
    def __init__(self, number_of_players):
        for i in range(1, number_of_players):
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
                self.pick_card() for i in range(self.number_of_pocket_cards)
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
        card_numbers.sort(reverse=True)  # Descending size
        card_numbers = sorted(
            card_numbers, key=lambda n: card_numbers.count(n), reverse=True)  # Descending frequency
        """TODO: MUST REMOVE DUPLICATE CARD NUMBER GROUPS HERE"""
        return card_numbers

    def get_highest_card(self, card_numbers):
        print(f"Ranked cards {self.sort_by_frequency_and_size(card_numbers)}")
        return self.sort_by_frequency_and_size(card_numbers)[0]

    def get_winner_from_ranked_hands(self, ranked_hands):
        card_numbers = self.get_card_numbers_from_highest_ranked_cards(
            ranked_hands)
        best_hand = self.get_highest_card(card_numbers)
        return best_hand




class GameRound(Players):
    """Player order represents the players' different positions in relation to
    the dealer around the table"""
    """Rotate the deque n steps to the right. If n is negative, rotate to the left."""

    highest_round_bet = 0
    pot = 0
    small_blind = 2
    big_blind = 4
    pre_flop_playing_order = deque(
        [player for player in Players.__dict__.keys()]
    )
    small_blind_player = pre_flop_playing_order[-2]
    big_blind_player = pre_flop_playing_order[-1]
    post_flop_playing_order = pre_flop_playing_order.rotate(2)
    dealer = post_flop_playing_order[-1]

    def adjust_player_order_after_round_end(self):
        self.playing_order(rotate=1)

    def play_blinds(self): -> Add to highest_bet Add to pot



    def ask_for_raise_call_fold(self):
        for player in self.pre_flop_playing_order:
            action = input(
                f"""{player}, 
                the highest bet of the round is{highest_round_bet}

    
        
        
    

    
    
    
    
    # Remove any people that fold from the post_flop_playing_order
   
   









    


 
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




    # ranked_hands = ClassifyHand().rank_hands(player_hands)
    # print(ranked_hands)
    # best_hand = FindBestHand().get_winner_from_ranked_hands(ranked_hands)
    # print(best_hand)
    # # Find which player has the best hand
    # # for k, v in player_and_cards:
    # #     card_numbers = FindBestHand().get_card_numbers_from_ranked_hand(hand)
    # #     if card_numbers == best_hand:
    # #         return

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







