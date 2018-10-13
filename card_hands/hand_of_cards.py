import random
import logging
logging.basicConfig(level=logging.INFO)

class GetCards:
    hand = []
    suites = ('H', 'D', 'S', 'C')

    def pick_card(self):
        card_number = random.randint(2, 14) # Aces are 14
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
        except TypeError: # This excepts where hand is None because no pair
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
        low_ace, high_ace = 1, 14
        card_numbers = set([card[0] for card in hand])
        logging.info(f"Before {card_numbers}")
        card_numbers = [low_ace if n == high_ace else n for n in card_numbers]
        card_numbers.sort()
        logging.info(f"After {card_numbers}")
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
        # Get each hand and assign it a rank
        ranked_hands = []
        for hand in hands:
            rank = self.rank_hand(sorted(hand))
            ranked_hands.append((rank, hand))
        return ranked_hands


    def get_highest_rank(self, ranked_hands):
        highest_rank = 0
        for ranked_hand in ranked_hands:
            if ranked_hand[0] > highest_rank:
                highest_rank = ranked_hand[0]
        return highest_rank

    def get_hands_with_the_highest_rank(self, ranked_hands):
        highest_rank = self.get_highest_rank(ranked_hands)
        hands_with_highest_rank = []
        for ranked_hand in ranked_hands:
            if ranked_hand[0] == highest_rank:
                hand_card_numbers = self.get_card_numbers_from_ranked_hand(
                    ranked_hand)
                hands_with_highest_rank.append(hand_card_numbers)
        print(hands_with_highest_rank)
        self.fail()
        return hands_with_highest_rank

    def get_card_numbers_from_ranked_hand(self, ranked_hand):
        print(ranked_hand)
        card_numbers = [card[0] for card in ranked_hand[1]]
        card_numbers.sort(reverse=True)
        return card_numbers

# Todo: Return the winner from the hands_with_the_highest_rank

        # Note Full house special case







    # Compare multiple hands and show the winner
    # Compare hand ranks
    # If same hand rank, look for highest card, i.e.,
    # If same highest card, look for second highest card, and so on.
    # If no winner, declare tie
    pass









if __name__ == "__main__":
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    print(new_hand.hand)





