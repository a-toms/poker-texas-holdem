import itertools
from collections import deque
import random
import time


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
        low_ace_n = 1
        high_ace_n = 14
        card_numbers = set([card.rank for card in hand])
        card_numbers = [low_ace_n if n == high_ace_n else n for n in card_numbers]
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

    def filter_hands_by_highest_score(self, hands: list) -> list:
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

    def get_winning_hands_from(self, raw_hands):
        hands_with_highest_score = self.filter_hands_by_highest_score(
            raw_hands
        )
        best_hand = self.get_hand_with_highest_card_rank(
            hands_with_highest_score
        )
        all_best_hands = [
            hand for hand in hands_with_highest_score
            if self.are_equal(
                self.get_card_ranks(best_hand),
                self.get_card_ranks(hand)
            )
        ]
        return all_best_hands

    def get_hand_with_highest_card_rank(self, filtered_hands: list) -> list:
        current_best_hand = filtered_hands[0]
        highest_ranks = self.get_card_ranks(filtered_hands[0])
        for hand in filtered_hands:
            challenger_ranks = self.get_card_ranks(hand)
            if self.is_higher(highest_ranks, challenger_ranks):
                current_best_hand = hand
                highest_ranks = challenger_ranks
        return current_best_hand

    def get_card_ranks(self, hand: list) -> list:
        return self.sort_by_frequency_and_size([card.rank for card in hand])

    @staticmethod
    def is_higher(current_n: list, challenger_n: list) -> bool:
        for a, b in zip(current_n, challenger_n):
            if a > b:
                return False
            if b > a:
                return True
        return False

    @staticmethod
    def are_equal(current_n: list, challenger_n: list) -> bool:
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
        self.hand_cards = []

    def generate_hand_combinations(self, card_dealer) -> itertools:
        card_pool = self.pocket_cards + card_dealer.table_cards
        return list(itertools.combinations(card_pool, r=5))

    def calculate_best_hand_for_player(self, card_dealer) -> list:
        if not card_dealer.table_cards:
            self.hand_cards = self.pocket_cards
            return self.hand_cards
        else:
            combinations = self.generate_hand_combinations(card_dealer)
            filtered = self.filter_hands_by_highest_score(combinations)
            self.hand_cards = self.get_hand_with_highest_card_rank(filtered)
            return self.hand_cards

    def print_best_hand(self):
        print(self.hand_cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.money = 1000
        self.amount_bet_during_stage = 0
        self.amount_bet_during_round = 0
        self.has_folded = False
        self.has_acted_during_stage = False
        self.in_big_blind_position = False
        self.in_small_blind_position = False
        self.in_dealer_position = False
        self.is_all_in = False
        self.max_winnings = 0

    def get_best_hand(self, card_dealer):
        return self.hand.calculate_best_hand_for_player(card_dealer)

    def __repr__(self):
        return f"{self.name} instance"

    def print_pocket_cards(self):
        print(f"pocket cards -> {self.hand.pocket_cards}")

    def print_status(self):
        print("----")
        print(f"{self.name.title()},\n" +
              f"You have {self.money} coins currently.\n" +
              f"You have bet {self.amount_bet_during_stage} " +
              f"this stage.\n"
              )

    def reset_for_new_round(self):
        self.amount_bet_during_stage = 0
        self.amount_bet_during_round = 0
        self.has_folded = False
        self.has_acted_during_stage = False
        self.in_big_blind_position = False
        self.in_small_blind_position = False
        self.in_dealer_position = False
        self.is_all_in = False
        self.max_winnings = 0


class Players:
    """
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
        self.hand_classifier = HandClassifier()
        self.winning_players = []
        try:
            self.dealer_player = self.playing_order[-3]
        except IndexError:  # Applies where there are only two players
            self.dealer_player = self.playing_order[-1]

    def reset_for_new_round(self):
        self.rotate_playing_order()
        self.highest_stage_bet = 0
        self.pot = 0
        self.assign_big_blind_player()
        self.assign_small_blind_player()
        self.winning_players = []

    def rotate_playing_order(self):
        self.playing_order.rotate(1)

    def instantiate_all_players(self):
        for i in range(1, self.number_of_players + 1):
            setattr(self, f'player{i}', Player(f'player{i}'))

    def store_players_in_register(self):
        return [
            value for value in self.__dict__.values()
            if type(value) == Player
        ]

    def assign_small_blind_player(self):
        """
        The small blind is second-last pre-flop and first post-flop.
        """
        self.small_blind_player: Player = self.playing_order[-2]
        self.small_blind_player.in_small_blind_position = True

    def assign_big_blind_player(self):
        """
        The big blind is last to act pre-flop and second to act post flop.
        """
        self.big_blind_player: Player = self.playing_order[-1]
        self.big_blind_player.in_big_blind_position = True

    def rotate_playing_order_before_flop(self):
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
            f"The big blind player, {self.big_blind_player.name.title()}, "
            f"paid the big blind of {self.big_blind}.\n" +
            f"The small blind player, {self.small_blind_player.name.title()}, "
            f"paid the small blind of {self.small_blind}.\n"
        )

    def reset_players_status_at_stage_end(self):
        for player_at_stage_end in self.playing_order:
            player_at_stage_end.amount_bet_during_stage = 0
            player_at_stage_end.has_acted_during_stage = False

    def reset_highest_stage_bet(self):
        self.highest_stage_bet = 0

    def get_any_player_that_is_all_in(self):
        for player in self.register:
            if player.money == 0:
                player.is_all_in = True
                yield player

    #todo: update for round bet
    def set_max_winnings_for_all_in_players(self):
        """Run at each stage's end."""
        for all_in_player in self.get_any_player_that_is_all_in():
            self.set_max_winnings_for_player(all_in_player)


    def set_max_winnings_for_player(self, all_in_player):
        """Creates an max winnings attribute for an all_in player.
        :type all_in_player: Player
        """
        for other_player in self.register:
            if (other_player.amount_bet_during_round >= all_in_player.amount_bet_during_round):
                all_in_player.max_winnings += all_in_player.amount_bet_during_round
            else:
                all_in_player.max_winnings += other_player.amount_bet_during_round


    def ask_all_players_for_actions(self):
        while self.at_least_one_player_must_act():
            for player in self.playing_order:
                if not self.at_least_two_players_left_in_round():
                    return
                if self.has_remaining_actions(player):
                    self.get_player_command(player)
                    self.mark_player_as_having_made_action(player)

    def is_there_any_default_winner(self):
        if not self.at_least_two_players_left_in_round():
            return True

    def set_any_default_winner(self):
        assert self.at_least_two_players_left_in_round() is False
        self.winning_players = self.get_each_not_folded_player()

    def at_least_two_players_left_in_round(self) -> bool:
        if len(self.get_each_not_folded_player()) < 2:
            return False
        else:
            return True

    def get_any_showdown_winner(self, card_dealer) -> list:
        return self.set_winning_players_based_on_winning_hands(card_dealer)

    def get_each_not_folded_player(self) -> list:
        return [
            player for player in self.playing_order
            if player.has_folded is False
        ]

    def set_winning_players_based_on_winning_hands(self, card_dealer) -> list:
        active_players = self.get_each_not_folded_player()
        players_best_hands = [
            active_player.get_best_hand(card_dealer)
            for active_player in active_players
        ]
        self.winning_players = [
            active_player
            for active_player in active_players
            if active_player.get_best_hand(card_dealer)
            in self.hand_classifier.get_winning_hands_from(players_best_hands)
        ]
        return self.winning_players

    def give_pot_to_winners(self):
        for winning_player in self.winning_players:
            winning_player.money += self.calculate_winnings_for(winning_player)

    def calculate_winnings_for(self, winning_player: Player):
        winnings = self.pot // len(self.winning_players)
        if winning_player.max_winnings != 0:
            if winnings > winning_player.max_winnings:
                return winning_player.max_winnings
        return winnings

    def print_winning_players(self):
        if len(self.winning_players) == 1:
            print(f"The winning player is {self.winning_players[0].name}")
        else:
            print("The winning players are ")
            for counter, winning_player in enumerate(self.winning_players):
                print(f"{winning_player.name}, ")
                if counter == len(self.winning_players) - 1:
                    print("and")

    def has_remaining_actions(self, player: Player) -> bool:
        if player.has_folded or player.is_all_in is True:
            return False
        if player.has_acted_during_stage and (
                player.amount_bet_during_stage == self.highest_stage_bet
        ):
            return False
        else:
            return True

    def at_least_one_player_must_act(self) -> bool:
        for player in self.register:
            if self.has_remaining_actions(player) is True:
                return True
        return False

    def get_player_command(self, player: Player):
        command = self.get_command(player)
        if self.is_command_valid(command) is True:
            self.execute_command(command, player)
        else:
            self.print_command_is_invalid()
            self.get_player_command(player)

    def get_command(self, player: Player):
        player.print_status()
        player.print_pocket_cards()  # Todo: consider refactoring more functions to be monadic like this
        try:
            command = int(input(
                "Would you like to check (0), call (1), raise (2), " +
                "or fold (3)? Enter command >>\n\n")
            )
        except ValueError:
            self.print_command_is_invalid()
            return self.get_command(player)
        return command

    def print_command_is_invalid(self):
        print("Your command is invalid.\n")

    @staticmethod
    def is_command_valid(command: int):
        if command not in [0, 1, 2, 3]:
            return False
        return True

    def execute_command(self, command, active_player):
        player_options = {
            0: self.check_bet,
            1: self.call_bet,
            2: self.raise_bet,
            3: self.fold_hand
        }
        return player_options[command](active_player)

    def call_bet(self, calling_player: Player) -> str:
        """This will make the player check if there is no higher bet."""
        call_amount = (
                self.highest_stage_bet -
                calling_player.amount_bet_during_stage
        )
        if calling_player.money - call_amount < 0:
            print(
                f"{calling_player.name.title()} "
                f"does not have enough money to call")
            return 'invalid action'
        calling_player.money -= call_amount
        calling_player.amount_bet_during_stage += call_amount
        calling_player.amount_bet_during_round += call_amount
        self.pot += call_amount
        print(f"{calling_player.name.title()} called {call_amount}.")
        return 'valid action'

    @staticmethod
    def fold_hand(folding_player: Player) -> bool:
        folding_player.has_folded = True
        print(f"{folding_player.name.title()} folded.")
        return True

    # todo: write test
    def raise_bet(self, raising_player: Player) -> bool:
        bet_amount = int(
            input(
                f"Enter the amount to raise above {self.highest_stage_bet}\n"
                f"(The highest bet during this stage is {self.highest_stage_bet})"
                f" >>\n"
            )
        )
        bet_amount += self.highest_stage_bet
        bet_amount -= raising_player.amount_bet_during_stage
        # todo: refactor this
        if raising_player.money - bet_amount < 0:
            print(
                f"Invalid bet. " +
                f"{raising_player.name.title()} does not have enough money."
            )
            return self.raise_bet(raising_player)
        else:
            self.place_bet(raising_player, bet_amount)
            print(
                f"{raising_player.name.title()} " +
                f"bet {raising_player.amount_bet_during_stage}"
            )
            return 'valid'

    def place_bet(self, raising_player: Player, bet_amount) -> bool:
        raising_player.money -= bet_amount
        raising_player.amount_bet_during_stage += bet_amount
        raising_player.amount_bet_during_round += bet_amount
        self.highest_stage_bet = raising_player.amount_bet_during_stage
        self.pot += bet_amount
        return True

    def check_bet(self, checking_player: Player) -> bool:
        if checking_player.amount_bet_during_stage == self.highest_stage_bet:
            return 'valid action'
        else:
            print(
                f"Invalid action. {checking_player.name.title()} " +
                "must match the highest current bet of " +
                f"{self.highest_stage_bet} to check"
            )
            return 'invalid action'

    @staticmethod
    def mark_player_as_having_made_action(player_who_made_action: Player):
        player_who_made_action.has_acted_during_stage = True

    def print_players_money(self):
        print("Player money:")
        for player in self.register:
            print(f"{player.name} has £{player.money}")


class CardDealer:
    def __init__(self):
        self.table_cards = []
        self.deck = self.generate_cards()

    def reset_for_new_round(self):
        self.table_cards = []

    @staticmethod
    def generate_cards():
        card_templates = itertools.product(range(2, 15), ('H', 'D', 'S', 'C'))
        return [Card(rank, suit) for rank, suit in card_templates]

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

    def __deal_card_to_table(self):
        card = self.pick_card()
        self.table_cards.append(card)

    def deal_flop(self):
        for i in range(3):
            self.__deal_card_to_table()

    def deal_turn(self):
        self.__deal_card_to_table()

    def deal_river(self):
        self.__deal_card_to_table()

    def show_table(self):
        print("______________________\n")
        print(f"Table cards : \n{self.table_cards}")
        print("______________________\n")


class Game:
    def __init__(self, number_of_players):
        self.n_players = number_of_players
        self.all_players = Players(self.n_players)
        self.card_dealer = CardDealer()
        self.hand_classifier = HandClassifier()

    # Todo: write test
    def execute_round_events(self):
        self.all_players.ask_all_players_for_actions()
        if self.all_players.is_there_any_default_winner() is True:
            self.all_players.set_any_default_winner()
            self.all_players.print_winning_players()
            self.all_players.give_pot_to_winners()
            return "end round"
        self.all_players.reset_players_status_at_stage_end()
        self.all_players.reset_highest_stage_bet()

    def run_pre_flop_events(self):
        self.card_dealer.deal_pocket_cards_to_players(self.all_players)
        self.all_players.pay_blinds()
        if self.execute_round_events() == "end round":
            return "end round"
        self.all_players.rotate_playing_order_before_flop()

    def run_flop_events(self):
        self.card_dealer.deal_flop()
        self.card_dealer.show_table()
        if self.execute_round_events() == "end round":
            return "end round"

    def run_turn_events(self):
        self.card_dealer.deal_turn()
        self.card_dealer.show_table()
        if self.execute_round_events():
            return "end round"

    def run_river_events(self):
        self.card_dealer.deal_river()
        self.card_dealer.show_table()
        if self.execute_round_events() == "end round":
            return "end round"
        self.all_players.get_any_showdown_winner(self.card_dealer)
        self.all_players.print_winning_players()
        self.all_players.give_pot_to_winners()

    @staticmethod
    def you_want_to_continue_game():
        seconds = 5
        while time.sleep(seconds):
            print(seconds)
            if input():
                return False
            seconds -= 1
        return True

    def run_round(self):
        if self.run_pre_flop_events() == "end round":
            return
        if self.run_flop_events() == "end round":
            return
        if self.run_turn_events() == "end round":
            return
        self.run_river_events()

    def play_game(self):
        self.run_round()
        self.run_post_round_events()

    def run_post_round_events(self):
        self.all_players.print_players_money()
        self.ask_if_you_want_to_continue_game()

    def ask_if_you_want_to_continue_game(self):
        print("Preparing for new round.Press X to end the game")
        self.you_want_to_continue_game()
        print("restart game")


if __name__ == "__main__":
    Game(3).play_game()
