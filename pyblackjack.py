import os
import random
import time

class Deck:
    def __init__(self):
        self.card_obj = {}
        self.suits = ["Heart", "Diamond", "Club", "Spade"]
        self.card_value = ["A" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.player_hand = []
        self.dealer_hand = []
        self.wager = ""
        self.bank = 100
        self.deck = self.build_deck()
        self.deal_deck = []

    def build_deck(self):
        print("Building Deck")
        deck = []
        for i in self.suits:
            for j in self.card_value:
                deck.append({"suit": i, "value": j})
        return deck
        
    def shuffle_deck(self, deck):
        """
        Fisher-Yates Shuffle algorithm
        """
        print(deck)
        for i in range(len(deck)-1, 0, -1):
            j = random.randint(0, i+1)
            deck[i], deck[j] = deck[j], deck[i]
        print(deck)
        return deck

    def deal(self):
        self.deal_deck = self.shuffle_deck(self.deck.copy())
        print(f"DEALER DECK {len(self.deal_deck)}")
        print(f"MASTER DECK {len(self.deck)}")
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
                print("Your Hand: ", self.player_hand)
                print("Dealer Is Showing", self.dealer_hand[1])
                return self.player_hand, self.dealer_hand
    
class GameOptions(Deck):
    def __init__(self):
        super().__init__()
        self.player_hand = []
        self.player_hand_value = int
        self.ace_count = 0
        self.split = False
        self.double_down = False
        self.decision = "False"
        self.player_options = ["HIT", "STAY", "SPLIT", "DD"]
    
    def available_options(self):
        # self.player_hand_value = self.score_check()
        if len(self.player_hand) > 2:
            self.user_input()
        else:
            self.check_split()
            self.check_double_down()
            self.user_input()

    def value_check(self, value):
        if value in ["J", "Q", "K"]:
            return 10
        elif value == "A":
            self.ace_count +=1
            return 11
        else:
            return value

    def ace_check(self, score):
        while self.ace_count > 0 and score > 21:
            score -= 10
            self.ace_count -= 1
        return score
        
    def end_game(self):
        print("You Lose")
        time.sleep(5)
        end_choice = ""
        while end_choice.upper() not in ["Y", "N"]:
            end_choice = input(f"You have ${self.bank} in the Bank\nPlay another hand?\n")
        if end_choice.upper() == "Y":
            print("running deck")
            self.deal()
            self.available_options()
        else:
            return "Game Over"


    def score_check(self):
        score = []
        for card in self.player_hand:
            value = self.value_check(card["value"])
            score.append(int(value))
            self.player_hand_value = sum(score)
            print(f"No ACE Check: {sum(score)}")
            new_score = self.ace_check(self.player_hand_value)
            print(f"ACE Check Score: {new_score}")
        if new_score > 21:
            self.end_game()
        else:
            self.available_options()

            
    def check_split(self):
        if self.player_hand[0]["value"] == self.player_hand[1]["value"]:
            self.split = True
        else:
            self.split = False
            print(type(self.player_options))
            for option in self.player_options:
                if option == "SPLIT":
                    self.player_options.remove(option)
                    print(self.player_options)
    
    def check_double_down(self):
        if len(self.player_hand) == 2: # add logic for split for double hands
            self.double_down = True
        else:
            self.double_down = False
            for option in self.player_options:
                if option == "DD":
                    self.player_options.remove(option)
                    print(self.player_options)

    def player_hit(self):
        print(f"DEALER DECK {len(self.deal_deck)}")
        print(f"MASTER DECK {len(self.deck)}")
        print(self.deal_deck)
        print(len(self.deal_deck))
        self.player_hand.append(self.deal_deck.pop(0))
        print(self.player_hand)
        self.score_check()
    
    def player_stay(self):
        pass

    def user_input(self):
        decision = ""
        while decision.upper() not in ["HIT", "STAY", "SPLIT", "DD"]:
            decision = input("What's Your Move? (HIT, STAY, SPLIT, DD)\n")
        if decision.upper() not in ["HIT", "STAY", "SPLIT", "DD"]:
            print(f"Sorry, '{decision}' is not an option provided...\nPlease Choose - HIT, STAY, SPLIT, or DD")
        if decision.upper() == "HIT":
            return self.player_hit()
        if decision.upper() == "STAY":
            return self.player_stay()


def start_new_game():

    # deck_client = Deck()
    game_client = GameOptions()
    print("Great! Let's Begin\nYou have $ {game_client.bank} in the bank\n")
    # deck_client.deal()
    game_client.deal()
    game_client.available_options()

def game_runner():
    choice = ""
    while choice.upper() not in ["Y", "N"]:
        choice = input("Hi User! Would You Like To Play BlackJack?: ")
        if choice.upper() not in ["Y", "N"]:
            print(f"Sorry! '{choice}' is not the answer I was looking for...\nPlease Enter Y or N")
    if choice.upper() == "Y":
        start_new_game()
    else:
        print("Okay! Run Program Again If You Would Like To Play!\nGoodbye!")
        return False

if __name__ == "__main__":
    game_runner()




