import random
import logging
logging.basicConfig(level=logging.INFO)


class GetCards:
    hand = []
    suites = ('H', 'D', 'S', 'C')

    def pick_card(self):
        card_number = random.randint(2, 14)  # Aces are 14
        suite = random.choice(self.suites)
        if (card_number, suite) in self.hand:
            self.pick_card()
        else:
            self.hand.append((card_number, suite))

    def pick_hand_of_cards(self, number_of_hand_cards):
        for i in range(number_of_hand_cards):
            self.pick_card()


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
        if len(set(card_suites)) == 1:
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
                hand_card_numbers = self.get_card_numbers_from_ranked_hand(
                    ranked_hand)
                hands_with_highest_rank.append(hand_card_numbers)
        return hands_with_highest_rank


    def get_card_numbers_from_ranked_hand(self, ranked_hand):
        """Convert a ranked hand to the hand's card numbers."""
        card_numbers = [card[0] for card in ranked_hand[1]]
        card_numbers = self.sort_by_frequency_and_size(card_numbers)
        return card_numbers


    def sort_by_frequency_and_size(self, card_numbers):
        card_numbers.sort(reverse=True)  # Ascending size
        card_numbers = sorted(
            card_numbers, key=lambda n: card_numbers.count(n), reverse=True)  # Ascending frequency
        return card_numbers


    def find_highest_card(self, card_numbers):
        # example input = [[6, 6, 6, 6, 2], [6, 6, 6, 6, 3], [6, 6, 6, 6, 1]]
        pass





""" Will require a method to match the highest card numbers to the particular
player. I like that the current methods will find the best hand in a 
player-neutral manner. The player-hand-matching method should be discrete"""

        





    # Compare multiple hands and show the winner
    # Compare hand ranks
    # If same hand rank, look for highest card, i.e.,
    # If same highest card, look for second highest card, and so on.
    # If no winner, declare tie




"""Game mechanics:

    1. Represent the board and pocket cards
    Have a board representation that the player can access, e.g.,
    board = [(3, 'H'), (3, 'C'), (4, 'S'), (14, 'C'), (8, 'H')], and
    deal pocket cards to each player, e.g.,
    hand = [(3, 'S'), (3, 'D').
    
    2. Find the best hand that the player can form. 
    
    Do this by running get_hand_rank for each permutation that the player can 
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
    
    
    
    """





if __name__ == "__main__":
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    print(new_hand.hand)





