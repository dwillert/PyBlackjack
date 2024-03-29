import os
import random
import time
from constants import SUITS, RANK

class Deck:
    """
    Class that creates the Playing Card Deck
    """

    def __init__(self):
        self.card_obj = {}
        self.player_hand = []
        self.dealer_hand = []
        self.wager = ""
        self.bank = float(100)
        self.deck = self.build_deck()
        self.deal_deck = []

    def build_deck(self):
        # print("Building Deck")
        deck = []
        for i in SUITS:
            for j in RANK:
                deck.append({"suit": i, "value": j})
        return deck

    def shuffle_deck(self, deck):
        """
        Fisher-Yates Shuffle algorithm
        """
        # print(deck)
        for i in range(len(deck)-1, 0, -1):
            j = random.randint(0, i+1)
            deck[i], deck[j] = deck[j], deck[i]
        # print(deck)
        return deck

    def deal(self):
        """
        Deals initial 4 cards and assigns them to the player and dealer hands
        """
        self.deal_deck = self.shuffle_deck(self.deck.copy())
        # print(f"DEALER DECK {len(self.deal_deck)}")
        # print(f"MASTER DECK {len(self.deck)}")
        count = 0
        self.dealer_hand = []
        self.player_hand = []
        for i in self.deal_deck:
            if count%2 == 0:
                self.player_hand.append(self.deal_deck.pop(count))
            else:
                self.dealer_hand.append(self.deal_deck.pop(count))
            count+=1
            if count == 4:
                # self.player_hand = [{'suit': 'Club', 'value': 'A'}, {'suit': 'Heart', 'value': 'A'}]
                print("Your Hand: ", self.player_hand)
                print("Dealer Is Showing: ", self.dealer_hand[1])
                return self.player_hand, self.dealer_hand

class GameOptions(Deck):
    def __init__(self):
        super().__init__()
        self.player_hand = []
        self.dealer_hand = []
        self.player_hand_value = int
        self.dealer_hand_value = int
        self.ace_count = 0
        self.dealer_ace_count = 0
        self.split = False
        self.double_down = False
        self.decision = "False"
        self.player_options = ["HIT", "STAY", "SPLIT", "DD"]

    def available_options(self):
        # self.player_hand_value = self.score_check()
        if len(self.player_hand) > 2:
            self.user_input()
            self.player_options = ["HIT", "STAY"]
        else:
            self.check_split()
            self.check_double_down()
            self.user_input()
        # print(self.player_options)

    def value_check(self, value):
        ace_count = 0
        if value in ["J", "Q", "K"]:
            return 10, ace_count
        elif value == "A":
            ace_count = 1
            return 11, ace_count
        else:
            return value, ace_count

    def ace_check(self, player_value):
        while self.ace_count > 0 and player_value > 21:
            player_value -= 10
            self.ace_count -= 1
        self.ace_count = 0
        return player_value

    def end_game(self, winner):
        if winner == "player":
            print("YOU WIN!")
            self.bank += self.wager
        elif winner == "player_ace":
            print("BLACKJACK!!")
            self.bank += self.wager * (3/2)
        else:
            print("YOU LOSE")
            self.bank -= self.wager
        print(f"You Now Have $ {self.bank}")
        time.sleep(5)
        end_choice = ""
        while end_choice.upper() not in ["Y", "N"]:
            end_choice = input(f"You have ${self.bank} in the Bank\nPlay another hand? [ Y, N ]\n")
        if end_choice.upper() == "Y":
            self.set_wager()
            self.deal()
            self.available_options()
        else:
            return "Game Over"

    def score_check(self):
        score = []
        for card in self.player_hand:
            value, ace_count = self.value_check(card["value"])
            self.ace_count += ace_count
            score.append(int(value))
            self.player_hand_value = sum(score)
            # player_value = sum(score)
        new_score = self.ace_check(self.player_hand_value)
        print(f"PLAYER Score: {new_score}")
        print("Dealer Is Showing: ", self.dealer_hand[1])
        if new_score > 21:
            self.end_game(winner="dealer")
        else:
            self.player_hand_value = new_score

    def check_split(self):
        if self.player_hand[0]["value"] == self.player_hand[1]["value"]:
            self.split = True
        else:
            self.split = False
            # print(type(self.player_options))
            for option in self.player_options:
                if option == "SPLIT":
                    self.player_options.remove(option)
                    # print(self.player_options)

    def check_double_down(self):
        if len(self.player_hand) == 2: # add logic for split for double hands
            self.double_down = True
        else:
            self.double_down = False
            for option in self.player_options:
                if option == "DD":
                    self.player_options.remove(option)
                    print(self.player_options)

    def player_double_down(self):
        self.wager += self.wager
        print(f"NOW WAGERING: ${self.wager}")
        self.player_hand.append(self.deal_deck.pop(0))
        print(self.player_hand)
        self.score_check()
        self.player_stay()

    def score_compare(self):
        print(f"PLAYER HAND: {self.player_hand_value}")
        print(f"DEALER HAND: {self.dealer_hand_value}")
        if self.dealer_hand_value == self.player_hand_value:
            print("PUSH")
            self.end_game(winner="push")
        elif self.dealer_hand_value > self.player_hand_value:
            print("DEALER WINS")
            self.end_game(winner="dealer")
        elif self.dealer_hand_value < self.player_hand_value:
            print("PLAYER WINS")
            self.end_game(winner="player")
        else:
            print("FIGURE IT OUT DAN")


    def dealer_score_check(self):
        print(self.dealer_hand)
        score = []
        for card in self.dealer_hand:
            value, ace_count = self.value_check(card["value"])
            self.dealer_ace_count += ace_count
            score.append(int(value))
            self.dealer_hand_value = sum(score)
        new_score = self.dealer_ace_check(self.dealer_hand_value)
        print(f"DEALER Score: {new_score}")
        if new_score > 21:
            self.end_game(winner="player")
        elif new_score == 21:
            print("Dealer got 21")
            self.end_game(winner="dealer")
        elif new_score <= 21 and new_score >= 16:
            print("dealer stays")
            self.dealer_hand_value = new_score
            self.score_compare()
        else:
            print("Dealer Hits")
            time.sleep(2)
            self.dealer_play()

    def dealer_ace_check(self, dealer_value):
        while self.dealer_ace_count > 0 and dealer_value > 21:
            dealer_value -= 10
            self.dealer_ace_count -= 1
        self.dealer_ace_count = 0
        return dealer_value

    def player_hit(self):
        self.player_hand.append(self.deal_deck.pop(0))
        print(self.player_hand)
        self.score_check()
        self.available_options()

    def dealer_play(self):
        print("DEALER PLAYS HAND")
        print(self.dealer_hand)
        time.sleep(5)
        self.dealer_hand.append(self.deal_deck.pop(0))
        print(self.dealer_hand)
        time.sleep(3)
        self.dealer_score_check()

    def player_stay(self):
        self.score_check()
        self.dealer_score_check()
        self.dealer_play()


    def user_input(self):
        decision = ""
        while decision.upper() not in self.player_options:
            decision = input(f"What's Your Move? {self.player_options}\n")
        if decision.upper() not in ["HIT", "STAY", "SPLIT", "DD"]:
            print(f"Sorry, '{decision}' is not an option provided...\nPlease Choose - HIT, STAY, SPLIT, or DD")
        if decision.upper() == "HIT":
            return self.player_hit()
        if decision.upper() == "STAY":
            return self.player_stay()
        if decision.upper() == "DD":
            return self.player_double_down()

    def wager_validation(self, input):
        try:
            wager = float(input)
            if wager < self.bank and wager > 0:
                print(f"MY WAGER: ${wager}")
                return wager
            else:
                print(f"{input} is not a valid wager\n")
                return False
        except:
            return False

    def set_wager(self):
        decision = ""
        while decision == "":
            decision = input("What's Your Wager?\n")
            wager_eval = self.wager_validation(decision)
            if wager_eval is not False:
                break
        print(type(wager_eval))
        self.wager = wager_eval

def start_new_game():
    """
    Starts a new game
    """
    # deck_client = Deck()
    game_client = GameOptions()
    print("Great! Let's Begin...\n")
    time.sleep(2)
    print(f"You have ${game_client.bank} in the bank\n")
    # deck_client.deal()
    game_client.set_wager()
    game_client.deal()
    game_client.available_options()

def game_runner():
    """
    Asks User Input to begin game
    """
    choice = ""
    while choice.upper() not in ["Y", "N"]:
        choice = input("Hi User! Would You Like To Play BlackJack?: [Y, N]\n")
        if choice.upper() not in ["Y", "N"]:
            print(f"Sorry! '{choice}' is not the answer I was looking for...\nPlease Enter Y or N\n")
    if choice.upper() == "Y":
        start_new_game()
    else:
        print("Okay! Run Program Again If You Would Like To Play!\nGoodbye!")
        return False

if __name__ == "__main__":
    game_runner()
    