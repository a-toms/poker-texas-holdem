import random


class GetCards:
    hand = []
    suites = ('H', 'D', 'S', 'C')

    def pick_card(self):
        card_number = random.randint(1, 13)
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
        if len(set(self.get_pairs(hand))) == 2:
            return set(self.get_pairs(hand))

    def get_three_of_a_kind(self, hand):
        card_numbers = [card[0] for card in hand]
        triples = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 3:
                triples += (card_number,)
        if triples != ():
            return triples

    def get_straight_with_no_ace_high(self, hand):
        card_numbers = list(set(sorted([card[0] for card in hand])))
        high_card, low_card = card_numbers[-1], card_numbers[0]
        if (len(card_numbers) == 5) and (high_card - low_card == 4):
            return tuple(card_numbers)

    def get_ace_high_straight(self, hand):
        """Add high ace (with card number 13) to sorted card numbers,
        delete the first card number, and then check for a straight"""
        card_numbers = list(set(sorted([card[0] for card in hand])))
        card_numbers.append(13)
        del card_numbers[0]
        high_card, low_card = card_numbers[-1], card_numbers[0]
        if (len(card_numbers) == 5) and (high_card - low_card == 4):
            return tuple(card_numbers)

    def get_straights(self, hand):
        straight_functions = (
            self.get_straight_with_no_ace_high,
            self.get_ace_high_straight
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

    hand_ranks = {
        GetHandRanks.get_straight_flush: (9, "straight_flush"),
        GetHandRanks.get_four_of_a_kind: (8, "four of a kind"),
        GetHandRanks.get_full_house: (7, "full house"),
        GetHandRanks.get_flush: (6, "flush"),
        GetHandRanks.get_straights: (5, "straight"),
        GetHandRanks.get_three_of_a_kind: (4, "three of a kind"),
        GetHandRanks.get_two_pairs: (3, "two pairs"),
        GetHandRanks.get_pairs: (2, "pair"),
        GetHandRanks.get_high_card: (1, "high card")
    }

    def rank_hand(self, hand):
        for f, rank_number in self.hand_ranks.items():
            if f(self, hand):
                return rank_number[0]

    def describe_hand(self, rank, hand):
        pass


    def show_winning_hand(self, hands):
        pass
    # Compare multiple hands and show the winner
    # Compare hand ranks
    # If same hand rank, look for highest card
    # If same highest card, look for second highest card, and so on.
    # If no winner, declare tie









if __name__ == "__main__":
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    test_hand = [
        (4, 'C'), (2, 'C'), (5, 'S'),
        (2, 'S'), (4, 'D')
    ]
    hand_ranker = GetHandRanks()
    results = hand_ranker.get_two_pairs(test_hand)
    print(results)





