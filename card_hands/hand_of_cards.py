import itertools
from collections import deque
import random
import logging

logging.basicConfig(level=logging.WARNING)

"""
TODO:

1a. Prune hand ranking and classifier classes COMPLETE
1. Find the winner; say the winner(s); give the pot to the winner(s)
    Winner may be the last player left or the player(s) with the highest card at the end of the stage.
2. Create game loops that allows players to play multiple hands.


Nomenclature:
The game consists of stages, which consist of stages.


"""


def print_output(func):
    def wrapper(*args):
        results = func(*args)
        print(f"output for {func.__name__} :\n{results} ")
        return results

    return wrapper


class Card:

    def __init__(self, rank: int, suit: str):
        self.ranks_representation = (
            None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
            "Queen", "King", "Ace"
        )
        self.suit_representation = {
            'D': 'Diamonds', 'S': 'Spades', 'C': 'Clubs', 'H': 'Hearts'
        }
        self.rank = rank
        self.suit = suit

    def return_rank_and_suit(self):
        return self.rank, self.suit

    def __repr__(self):
        return f"{self.ranks_representation[self.rank]} of {self.suit_representation[self.suit]}"


class HandRanker:

    def get_high_card(self, hand):
        card_numbers = tuple(set([card.rank for card in hand]))
        return tuple(sorted(card_numbers))

    def get_pairs(self, hand):
        card_numbers = [card.rank for card in hand]
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
        card_numbers = [card.rank for card in hand]
        triples = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 3:
                triples += (card_number,)
        if triples != ():
            return triples

    def get_straight_with_low_ace(self, hand):
        """
        Check if a straight exists if the ace is treated as a low ace.
        hand is an iterable of Card instances.
        """
        low_ace, high_ace = 1, 14
        card_numbers = set([card.rank for card in hand])
        card_numbers = [low_ace if n == high_ace else n for n in card_numbers]
        card_numbers.sort()
        high_card, low_card = card_numbers[-1], card_numbers[0]
        if len(card_numbers) == 5 and high_card - low_card == 4:
            return tuple(card_numbers)

    def get_straight_without_low_ace(self, hand):
        card_numbers = list(set(sorted([card.rank for card in hand])))
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
        card_suites = tuple([card.suit for card in hand])
        card_numbers = [card.rank for card in hand]
        if len(card_numbers) == 5 and len(set(card_suites)) == 1:
            return card_suites[1]

    def get_full_house(self, hand):
        card_numbers = tuple([card.rank for card in hand])
        if self.get_three_of_a_kind(hand) is not None:
            if self.get_pairs(hand):
                return tuple(card_numbers)

    def get_four_of_a_kind(self, hand):
        card_numbers = [card.rank for card in hand]
        quads = ()
        for card_number in card_numbers:
            if card_numbers.count(card_number) == 4:
                quads += (card_number,)
        if quads != ():
            return quads

    def get_straight_flush(self, hand):
        if self.get_straights(hand) and self.get_flush(hand):
            return sorted(hand, key=lambda n: n.rank)

    hand_ranks = {
        get_straight_flush: 9,
        get_four_of_a_kind: 8,
        get_full_house: 7,
        get_flush: 6,
        get_straights: 5,
        get_three_of_a_kind: 4,
        get_two_pairs: 3,
        get_pairs: 2,
        get_high_card: 1
    }

    def rank_hand(self, hand: list) -> int:
        for f, rank in self.hand_ranks.items():
            if f(self, hand):
                return rank

    def rank_hands(self, hands):
        """Get each hand and assign it a rank."""
        ranked_hands = []
        for hand in hands:
            rank = self.rank_hand(sorted(hand, key=lambda n: n.rank))
            ranked_hands.append((rank, hand))
        return ranked_hands


class HandClassifier(HandRanker):

    def filter_hands_by_highest_score(self, hands) -> list:
        high_score = self.get_highest_hand_score(hands)
        return [
            hand for hand in hands
            if self.rank_hand(hand) == high_score
        ]

    def get_highest_hand_score(self, hands) -> int:
        highest_hand_score = 0
        for hand in hands:
            if self.rank_hand(hand) >= highest_hand_score:
                highest_hand_score = self.rank_hand(hand)
        return highest_hand_score

    @print_output
    def get_hand_with_highest_card_rank(self, filtered_hands: list) -> list:
        # Returns
        current_best_hand = filtered_hands[0]
        highest_ranks = self.get_card_ranks(filtered_hands[0])
        for hand in filtered_hands:
            challenger_ranks = self.get_card_ranks(hand)
            if self.is_challenger_higher(highest_ranks, challenger_ranks):
                current_best_hand = hand
                highest_ranks = challenger_ranks
        return current_best_hand

    def get_card_ranks(self, hand: list) -> list:
        return self.sort_by_frequency_and_size([card.rank for card in hand])

    # Todo: write test
    def get_all_best_hands(self, raw_hands):
        hands_with_highest_score = self.filter_hands_by_highest_score(
            raw_hands
        )
        best_hand = self.get_hand_with_highest_card_rank(
            hands_with_highest_score
        )
        all_best_hands = [
            hand for hand in hands_with_highest_score
            if self.is_challenger_equal(
                best_hand,
                hand
            )
        ]
        return all_best_hands

    # Todo: write test
    @staticmethod
    def is_challenger_higher(current_n: list, challenger_n: list) -> bool:
        for a, b in zip(current_n, challenger_n):
            if a > b:
                return False
            if b > a:
                return True
        return False

    # Todo: write test
    @staticmethod
    def is_challenger_equal(current_n: list, challenger_n: list) -> bool:
        for a, b in zip(current_n, challenger_n):
            if a > b:
                return False
            if b > a:
                return False
        return True

    @staticmethod
    def sort_by_frequency_and_size(numbers):
        """Sort by descending frequency and descending size."""
        numbers.sort(reverse=True)
        numbers = sorted(
            numbers, key=lambda n: numbers.count(n), reverse=True
        )
        return numbers


class Hand(HandClassifier):

    def __init__(self):
        self.pocket_cards = []
        self.highest_hand_score = 0
        self.best_hand = []

    def generate_hand_combinations(self, card_dealer) -> itertools:
        card_pool = self.pocket_cards + card_dealer.table_cards
        return list(itertools.combinations(card_pool, r=5))

    def calculate_best_hand_for_player(self, card_dealer) -> list:
        if not card_dealer.table_cards:
            self.best_hand = self.pocket_cards
            return self.best_hand
        else:
            combinations = self.generate_hand_combinations(card_dealer)
            filtered = self.filter_hands_by_highest_score(combinations)
            self.best_hand = self.get_hand_with_highest_card_rank(filtered)
            return self.best_hand

    def print_best_hand(self):
        print(self.best_hand)

    def print_pocket_cards(self):
        print(self.pocket_cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.money = 100
        self.amount_bet_during_stage = 0
        self.has_folded_hand = False
        self.has_acted_during_stage = False
        self.in_big_blind_position = False
        self.in_small_blind_position = False
        self.in_dealer_position = False
        self.is_all_in = False
        self.max_winnings = 0  # Todo: integrate with the awarding of the pot

    def get_best_hand(self, card_dealer):
        return self.hand.calculate_best_hand_for_player(card_dealer)

    def __repr__(self):
        return f"{self.name} instance"


class Players:
    """
    Includes functions that apply to multiple players
    Use .register to access the different players in Players.
    """

    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.instantiate_all_players()
        self.register = self.store_players_in_register()
        self.playing_order = deque(
            player for player in self.register
        )
        self.highest_stage_bet = 0
        self.pot = 0
        self.small_blind = 20
        self.big_blind = 40
        self.assign_big_blind_player()
        self.assign_small_blind_player()
        try:
            self.dealer_player = self.playing_order[-3]
        except IndexError:  # Applies where there are only two players
            self.dealer_player = self.playing_order[-1]

    def instantiate_all_players(self) -> None:
        for i in range(1, self.number_of_players + 1):
            setattr(self, f'player{i}', Player(f'player{i}'))

    def store_players_in_register(self):
        return [
            value for value in self.__dict__.values()
            if type(value) == Player
                         ]

    def assign_small_blind_player(self) -> None:
        """
        The small blind is second-last pre-flop and first post-flop.
        """
        self.small_blind_player: Player = self.playing_order[-2]
        self.small_blind_player.in_small_blind_position = True

    def assign_big_blind_player(self) -> None:
        """
        The big blind is last to act pre-flop and second to act post flop.
        """
        self.big_blind_player: Player = self.playing_order[-1]
        self.big_blind_player.in_big_blind_position = True

    def rotate_playing_order_before_flop(self) -> None:
        """
        Rotates playing order by 2 to begin from the left of the
        dealer player.
        """
        self.playing_order.rotate(2)

    def pay_blinds(self):
        self.small_blind_player.money -= self.small_blind
        self.small_blind_player.amount_bet_during_stage += self.small_blind
        self.big_blind_player.money -= self.big_blind
        self.big_blind_player.amount_bet_during_stage += self.big_blind
        self.pot += self.big_blind + self.small_blind
        self.highest_stage_bet = self.big_blind
        self.print_blinds_message()

    def print_blinds_message(self):
        print(
            f""
            f"The big blind player, {self.big_blind_player.name.title()}, "
            f"paid the big blind of {self.big_blind}.\n" +
            f"The small blind player, {self.small_blind_player.name.title()}, "
            f"paid the small blind of {self.small_blind}.\n"
        )

    def print_request(self, active_player: Player) -> None:
        print(f"\n{active_player.name.title()},\n" +
              f"You have {active_player.money} coins currently.\n" +
              f"You have bet {active_player.amount_bet_during_stage} " +
              f"this stage.\n" +
              f"The highest bet of the stage so far " +
              f"is {self.highest_stage_bet}.\n"
              )

    def give_pot_to_winners(self, winners):
        winnings = self.pot // len(winners)
        for player in winners:
            self.__dict__[player].money += winnings
        self.pot = 0

    def reset_players_status_at_stage_end(self):
        for player_at_stage_end in self.playing_order:
            player_at_stage_end.amount_bet_during_stage = 0
            player_at_stage_end.has_acted_during_stage = False

    def reset_highest_stage_bet(self):
        self.highest_stage_bet = 0

    def get_any_player_that_is_all_in(self):
        for player in self.register:
            if player.is_all_in:
                yield player

    def set_max_winnings_for_all_in_players(self):
        """Run at each stage's end."""
        if self.get_any_player_that_is_all_in() is not None:
            for all_in_player in self.get_any_player_that_is_all_in():
                self.set_max_winnings_for_player(all_in_player)

    def set_max_winnings_for_player(self, all_in_player: Player) -> None:
        """Creates an max winnings attribute for an all_in player."""
        for other_player in self.register:
            if other_player.amount_bet_during_stage >= all_in_player.amount_bet_during_stage:
                all_in_player.max_winnings += all_in_player.amount_bet_during_stage
            else:
                all_in_player.max_winnings += other_player.amount_bet_during_stage

    def ask_all_players_for_actions(self) -> None:
        while self.at_least_one_player_must_act() is True:
            for player in self.playing_order:
                if self.has_remaining_actions(player) is True:
                    self.get_player_command(player)
                    self.mark_player_as_having_made_action(player)

    # Todo: write test
    def get_any_default_winner(self):
        if not self.at_least_two_players_left_in_round():
            return self.find_each_not_folded_player()
        else:
            return None

    # Todo: write test
    def at_least_two_players_left_in_round(self):
        if len(self.find_each_not_folded_player()) < 2:
            return self.find_each_not_folded_player()
        else:
            return False

    # Todo: write test
    def get_any_showdown_winner(self, card_dealer) -> list:
        active_players = self.find_each_not_folded_player()
        best_hands = self.get_best_hand_of_each_player(
            active_players, card_dealer
        )
        winners = self.identify_players_with_the_best_hands(
            active_players, best_hands
        )
        return winners

    # Todo: write test
    def find_each_not_folded_player(self) -> list:
        return [
            player for player in self.playing_order
            if player.has_folded_hand is False
        ]

    # Todo: write test
    def get_best_hand_of_each_active_player(
            self, active_players, card_dealer) -> list:
        return [
            active_player.get_best_hand(card_dealer)
            for active_player in active_players
        ]

    # Todo: write test
    @staticmethod
    def identify_players_with_the_best_hands(
            active_players, best_hands) -> list:
        players_with_the_best_hands = [
            active_player
            for active_player in active_players
            if active_player.get_best_hand() in best_hands
        ]
        return players_with_the_best_hands

    def has_remaining_actions(self, player: Player) -> bool:
        if player.has_folded_hand or player.is_all_in is True:
            return False
        elif player.amount_bet_during_stage == self.highest_stage_bet and player.has_acted_during_stage is True:
            return False
        else:
            return True

    def at_least_one_player_must_act(self) -> bool:
        for player in self.register:
            if self.has_remaining_actions(player) is True:
                return True
        return False

    def get_player_command(self, player: Player) -> None:
        action = self.get_player_input(player)
        valid_command_exists = self.perform_player_command(action, player)
        if valid_command_exists is False:
            self.get_player_command(player)

    def get_player_input(self, player: Player) -> str:
        self.print_request(player)
        command = input(
            "Would you like to check (0), call (1), raise (2), " +
            "or fold (3)? Enter command >>\n\n")
        return command

    def perform_player_command(self, command: str, active_player: Player):
        if command is '0':
            return self.check_bet(active_player)
        elif command is '1':
            return self.call_bet(active_player)
        elif command is '2':
            return self.get_amount_to_raise(active_player)
        elif command is '3':
            return self.fold_hand(active_player)
        else:
            print("Your command is invalid.\n")
            return False

    def call_bet(self, calling_player: Player) -> bool:
        """This will make the player check if there is no higher bet."""
        call_amount = (
                self.highest_stage_bet -
                calling_player.amount_bet_during_stage
        )
        if calling_player.money - call_amount < 0:
            print(
                f"{calling_player.name.title()} "
                f"does not have enough money to call")
            return False
        calling_player.money -= call_amount
        calling_player.amount_bet_during_stage += call_amount
        self.pot += call_amount
        print(f"{calling_player.name.title()} called {call_amount}.")
        return True

    @staticmethod
    def fold_hand(folding_player: Player) -> bool:
        folding_player.has_folded_hand = True
        print(f"{folding_player.name.title()} folded.")
        return True

    def get_amount_to_raise(self, raising_player: Player) -> bool:
        bet_amount: int = int(input("Enter the amount to raise >>\n"))
        if self.highest_stage_bet > bet_amount + raising_player.amount_bet_during_stage:
            print(f"Insufficient bet. The bet must be larger to raise. " +
                  f"Try again")
            return False
        if raising_player.money - bet_amount < 0:
            print(f"Invalid bet. " +
                  f"{raising_player.name.title()} does not have enough money.")
            return False
        else:
            self.place_bet(raising_player, bet_amount)
            print(f"{raising_player.name.title()} raised {bet_amount} " +
                  f"to bet {raising_player.amount_bet_during_stage} overall.")
            return True

    def place_bet(self, raising_player: Player, bet_amount) -> bool:
        raising_player.money -= bet_amount
        raising_player.amount_bet_during_stage += bet_amount
        self.highest_stage_bet = raising_player.amount_bet_during_stage
        self.pot += bet_amount
        return True

    def check_bet(self, checking_player: Player) -> bool:
        if checking_player.amount_bet_during_stage == self.highest_stage_bet:
            return True
        else:
            print(
                f"Invalid action. {checking_player.name.title()}" +
                "must match the highest current bet of " +
                f"{self.highest_stage_bet} to check"
            )
            return False

    @staticmethod
    def mark_player_as_having_made_action(player_who_made_action: Player):
        player_who_made_action.has_acted_during_stage = True


class CardDealer:
    def __init__(self, number_of_starting_players):
        self.table_cards = []
        self.number_of_starting_players = number_of_starting_players
        self.deck = self.generate_cards()

    @staticmethod
    def generate_cards():
        card_templates = itertools.product(range(2, 15), ('H', 'D', 'S', 'C'))
        return [Card(rank, suit) for rank, suit in card_templates]

    # Todo: write test
    def pick_card(self) -> Card:
        random.shuffle(self.deck)
        return self.deck.pop()

    def deal_pocket_cards_to_player(self, receiving_player: Player) -> None:
        for i in range(2):
            picked_card = self.pick_card()
            receiving_player.hand.pocket_cards.append(picked_card)

    def deal_pocket_cards_to_players(self, receiving_players: Players) -> None:
        for receiving_player in receiving_players.register:
            self.deal_pocket_cards_to_player(receiving_player)

    def deal_card_to_table(self):
        card = self.pick_card()
        self.table_cards.append(card)

    def deal_flop(self):
        for i in range(3):
            self.deal_card_to_table()

    def deal_turn(self):
        self.deal_card_to_table()

    def deal_river(self):
        self.deal_card_to_table()

    def show_table(self):  # Basic
        print("______________________\n")
        print(f"Table cards : \n{self.table_cards}")
        print("______________________\n")


class BasicDisplay:
    # Todo: create basic GUI

    def print_table(self):
        print(f"Table cards : "
              f"\n")  # Refer to table cards

    def print_header(self):
        print("________________________________________________\n")
        print("| Pocket Cards | Bet | Status | Position |")

    def print_player_stats(self, player):
        print(f"{player.hand.pocket_cards} | *FILLER* | *FILLER* | *FILLER* ")



if __name__ == "__main__":
    """
    3 main objects: 1. player; 2. all_players, 3. card_dealer;    
    """

    n_of_players = 8
    all_players = Players(n_of_players)
    card_dealer = CardDealer(n_of_players)
    card_dealer.deal_pocket_cards_to_players(all_players)

    all_players.pay_blinds()
    all_players.ask_all_players_for_actions()
    # check for default winner
    all_players.reset_players_status_at_stage_end()
    all_players.reset_highest_stage_bet()
    all_players.rotate_playing_order_before_flop()

    card_dealer.deal_flop()
    card_dealer.show_table()
    all_players.ask_all_players_for_actions()
    # check for default winner
    all_players.reset_players_status_at_stage_end()
    all_players.reset_highest_stage_bet()

    card_dealer.deal_turn()
    card_dealer.show_table()
    all_players.ask_all_players_for_actions()
    # check for default winner
    all_players.reset_players_status_at_stage_end()
    all_players.reset_highest_stage_bet()

    card_dealer.deal_river()
    card_dealer.show_table()
    all_players.ask_all_players_for_actions()
    # check for default winner
    # find winner
    # Todo: announce winner and pay pot
