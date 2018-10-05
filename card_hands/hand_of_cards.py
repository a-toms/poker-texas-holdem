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


class GetHandRankings:

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

    def get_four_of_a_kind(self, hand):
        card_numbers = [card[0] for card in hand]
        quads = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 4:
                quads += (card_number,)
        if quads != ():
            return quads

    def get_full_house(self, hand):
        card_numbers = tuple([card[0] for card in hand])
        if self.get_three_of_a_kind(hand) is not None:
            if self.get_pairs(hand):
                return tuple(card_numbers)

    def get_straight_with_no_ace_high(self, hand):
        card_numbers = sorted([card[0] for card in hand])
        high_card_number, low_card_number = card_numbers[-1], card_numbers[0]
        if high_card_number - low_card_number == 4:
            return tuple(card_numbers)

    def get_ace_high_straight(self, hand):
        """Add high ace (with card number 13) to sorted card numbers,
        delete the first card number, and then check for a straight"""
        card_numbers = sorted([card[0] for card in hand])
        card_numbers.append(13)
        del card_numbers[0]
        high_card_number, low_card_number = card_numbers[-1], card_numbers[0]
        if high_card_number - low_card_number == 4:
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

    def get_straight_flush(self, hand):
        if self.get_straights(hand) and self.get_flush(hand):
            return sorted(hand)











if __name__ == "__main__":
    new_hand = GetCards()
    new_hand.pick_hand_of_cards(52)
    test_hand = [
        (4, 'C'), (2, 'C'), (5, 'S'),
        (2, 'S'), (4, 'D')
    ]
    hand_ranker = GetHandRankings()
    results = hand_ranker.get_two_pairs(test_hand)
    print(results)





