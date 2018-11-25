import itertools
from collections import deque
import random
import logging

logging.basicConfig(level=logging.INFO)

"""
TODO:

1. Build one working game round (including tests)
2. Refactor to pass Player instances around, rather than using state

"""


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

    def get_card_numbers_from_cards_in_highest_rank(self, ranked_hands):
        """
        Return card numbers from only the hands with the highest rank.
        """
        highest_rank = self.get_highest_rank(ranked_hands)
        hands_with_highest_rank = []
        for ranked_hand in ranked_hands:
            if ranked_hand[0] == highest_rank:
                hands_with_highest_rank.append(
                    self.get_card_numbers_from_ranked_hand(ranked_hand)
                )
        return hands_with_highest_rank

    def get_card_numbers_from_ranked_hand(self, ranked_hand):
        """
        Convert a ranked hand to the hand's card numbers.
        """
        card_numbers = [card[0] for card in ranked_hand[1]]
        print(card_numbers)
        card_numbers = self.sort_by_frequency_and_size(card_numbers)
        return card_numbers

    def sort_by_frequency_and_size(self, card_numbers):
        """
        Sort into descending card number size and descending frequency.
        """
        card_numbers.sort(reverse=True)
        card_numbers = sorted(
            card_numbers, key=lambda n: card_numbers.count(n), reverse=True
        )
        return card_numbers

    def get_highest_card(self, card_numbers):
        card_numbers = self.filter_out_duplicates(card_numbers)
        return self.sort_by_frequency_and_size(card_numbers)[0]

    def get_winner_from_ranked_hands(self, ranked_hands: tuple):
        card_numbers = self.get_card_numbers_from_cards_in_highest_rank(
            ranked_hands)
        best_hand = self.get_highest_card(card_numbers)
        return best_hand

    def filter_out_duplicates(self, iterable):
        filtered = []
        for x in iterable:
            if x not in filtered:
                filtered.append(x)
        return filtered


class Player: # Todo: Modify player to incorporate hand ranking within the class
    money = 100
    amount_bet_in_round = 0
    pocket_cards = []
    current_hand = []
    has_folded_hand = False
    has_acted_in_round = False
    in_big_blind_position = False
    in_small_blind_position = False
    in_dealer_position = False


    def __init__(self, name):
        self.name = name

    def get_best_current_hand(self):
        pass
    #todo: find the best current hand
    #itertools.permutations



class Players(Player):
    """
    Use __dict__ to access the different players in Players.
    """
    def __init__(self, number_of_players):
        for i in range(1, number_of_players + 1):
            setattr(self, f'player{i}', Player(f'player{i}'))


class CardDealer:
    dealt_cards = []
    table_cards = []

    def __init__(self, number_of_starting_players):
        self.number_of_starting_players = number_of_starting_players
        self.deck = list(itertools.product(range(2, 15), ('H', 'D', 'S', 'C')))

    def pick_card(self) -> tuple:
        card = random.choice(self.deck)
        self.deck.remove(card)
        self.dealt_cards.append(card)
        return card

    def deal_pocket_cards(self, active_players) -> None:
        for player in active_players.__dict__.values():
            player.pocket_cards.append(self.pick_card())
            player.pocket_cards.append(self.pick_card())

    def deal_flop(self):
        for i in range(3):
            card = self.pick_card()
            self.table_cards.append(card)

    def deal_card_to_table(self):
        card = self.pick_card()
        self.table_cards.append(card)

    def deal_turn(self):
        self.deal_card_to_table()

    def deal_river(self):
        self.deal_card_to_table()

    def show_table(self): # Basic
        print(f"Table cards : \n{self.table_cards}")


class GameRound:
    """
    .players_information contains all of the Player instances.
    .card_dealer contains card dealer functions.
    .player_position_order contains a deque of Player instances.
    .player_order contains a deque of Player instances.

    """
    highest_round_bet = 0
    pot = 0
    small_blind = 20
    big_blind = 40

    def __init__(self, instantiated_players, instantiated_dealer):
        self.players_information = instantiated_players
        self.card_dealer = instantiated_dealer
        self.playing_order = deque(
            player for player in self.players_information.__dict__.values()
        )
        self.assign_big_blind_player()
        self.assign_small_blind_player()
        try:
            self.dealer_player = self.playing_order[-3]
        except IndexError:  # Applies where there are only two players
            self.dealer_player = self.playing_order[-1]

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


    def rotate_playing_order_before_flop(self) -> None:
        """
        Rotates playing order by 2 to begin from the left of the
        dealer player.
        """
        self.playing_order.rotate(2)

    def pay_blinds(self):
        self.small_blind_player.money -= self.small_blind
        self.small_blind_player.amount_bet_in_round += self.small_blind
        self.big_blind_player.money -= self.big_blind
        self.big_blind_player.amount_bet_in_round += self.big_blind
        self.pot += self.big_blind + self.small_blind
        self.highest_round_bet = self.big_blind
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
              f"You have bet {active_player.amount_bet_in_round} " +
              f"this round.\n" +
              f"The highest bet of the round so far " +
              f"is {self.highest_round_bet}.\n"
              )

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
        """
        This will make the player effectively check if there is no higher bet.
        """
        call_amount = (
                self.highest_round_bet -
                calling_player.amount_bet_in_round
        )
        if calling_player.money - call_amount < 0:
            print(f"{calling_player.name.title()} does not have enough money to call")
            return False
        calling_player.money -= call_amount
        calling_player.amount_bet_in_round += call_amount
        self.pot += call_amount
        print(f"{calling_player.name.title()} called {call_amount}.")
        return True

    def fold_hand(self, folding_player: Player) -> bool:
        folding_player.has_folded_hand = True
        print(f"{folding_player.name.title()} folded.")
        return True

    def get_amount_to_raise(self, raising_player: Player) -> bool:
        bet_amount: int = int(input("Enter the amount to raise >>\n"))
        if self.highest_round_bet > bet_amount + raising_player.amount_bet_in_round:
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
                  f"to bet {raising_player.amount_bet_in_round} overall.")
            return True

    def place_bet(self, raising_player: Player, bet_amount) -> bool:
        raising_player.money -= bet_amount
        raising_player.amount_bet_in_round += bet_amount
        self.highest_round_bet = raising_player.amount_bet_in_round
        self.pot += bet_amount
        return True

    def check_bet(self, checking_player: Player) -> bool:
        if checking_player.amount_bet_in_round == self.highest_round_bet:
            return True
        else:
            print(f"Invalid action. {checking_player.name.title()} must match the highest current bet " +
                  f"of {self.highest_round_bet} to check")
            return False

    def give_pot_to_winners(self, winners: tuple) -> None:  # Pass in the Player objects
        winnings = self.pot // len(winners)
        for player in winners:
            self.players_information.__dict__[player].money += winnings
        self.pot = 0

    def mark_player_as_having_made_action(self, player_who_made_action: Player):
        player_who_made_action.has_acted_in_round = True

    def has_remaining_actions(self, player: Player) -> bool:
        if player.has_folded_hand is True:
            return False
        elif player.amount_bet_in_round == self.highest_round_bet and player.has_acted_in_round is True:
            return False
        else:
            return True

    def at_least_one_player_has_remaining_action(self) -> bool: #Todo: write test.
        for player in self.players_information.__dict__.values():
            if self.has_remaining_actions(player) is True:
                return True
        return False

    def ask_all_players_for_actions(self, player_order: dict) -> None:  #Todo: write test.
        while self.at_least_one_player_has_remaining_action() is True:
            for player in player_order:
                if self.has_remaining_actions(player) is True:
                    self.get_player_command(player)
                    self.mark_player_as_having_made_action(player)

    def reset_players_status_at_round_end(self):
        for player_at_round_end in self.playing_order:
            player_at_round_end.amount_bet_in_round = 0
            player_at_round_end.has_acted_in_round = False

    def reset_highest_round_bet(self):
        self.highest_round_bet = 0






if __name__ == "__main__":
    """
    3 main objects: 1. all_players, 2. card_dealer; 3. game_round.
    
    May refactor the below to reduce the sprawling dominance of game_round.
    """
    n_of_players = 8
    all_players = Players(n_of_players)
    card_dealer = CardDealer(n_of_players)
    game_round = GameRound(all_players, card_dealer)
    print(game_round.players_information.player1.hand)
    card_dealer.deal_pocket_cards(all_players)
    game_round.pay_blinds()
    game_round.ask_all_players_for_actions(game_round.playing_order)
    game_round.reset_players_status_at_round_end()
    game_round.rotate_playing_order_before_flop()

    game_round.card_dealer.deal_flop()
    game_round.card_dealer.show_table()
    game_round.ask_all_players_for_actions(game_round.playing_order)
    game_round.reset_players_status_at_round_end()

    game_round.card_dealer.deal_turn()
    game_round.card_dealer.show_table()
    game_round.ask_all_players_for_actions(game_round.playing_order)
    game_round.reset_players_status_at_round_end()

    game_round.card_dealer.deal_river()
    game_round.card_dealer.show_table()
    game_round.ask_all_players_for_actions(game_round.playing_order)
