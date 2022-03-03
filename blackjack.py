from copy import deepcopy
from random import betavariate, randrange
import os

class Blackjack():
    SHOWING = 0
    HIDDEN = 1

    HIT = 0
    STAND = 1
    SPLIT = 2
    DOUBLE_DOWN = 3

    def __init__(self, bet, deck_count):
        # Master deck copied to make a game deck
        self.master_deck = self.__build_deck(deck_count)
        self.playing = False                    # game in progress?
        self.logs = False                       # display logs?
        self.bet = bet                          # possible reward for winning/losing                          
        self.deck = []                          # current game deck
        self.player_hand = []                   # cards in the players hand
        self.dealer_hand = []                   # cards in the dealers hand ([0] = SHOWING)
        self.split_hand = []                    # cards in the split hand (if applicable)
        self.player_hand_sum = 0                # total value of player hand
        self.dealer_hand_sum = 0                # total value of dealer hand 
        self.split_hand_sum = 0                 # total value of split hand (if applicable)
        self.round = 0                          # game round    
        self.final_reward = 0                   # unused atm
        self.split = False                      # is there a split hand?
        self.split_active = False               # is current hand being played a split hand?

    def __build_deck(s, deck_count):
        deck = []
        # Add 4 cards for each numbered value A - 9 to the deck
        for card in range(1,10):
            deck.append(4*deck_count)
        # Add 4 cards of value 10 for 10, J, Q, K
        for tens in range(4):
            deck.append(4*deck_count)
        return(deck)

    def build_state(s, hand):
        # Initially set state to sum of the card values
        hand_sum = sum(hand)
        # If hand != [A, 10] check for an ace ([A,A] = [1,11])
        if (hand_sum != 21):
            if (hand[0] == 11):
                hand_sum += 10
            elif (hand[1] == 11):
                hand_sum += 10
            else:
                hand_sum = sum(hand)
        return tuple([hand_sum, s.dealer_hand[s.SHOWING]])

    def start_hand(s):
        s.playing = True
        s.split_active = False 
        s.split = False
        s.deck = deepcopy(s.master_deck)
        s.player_hand = [0,0]
        s.dealer_hand = [0,0]
        s.split_hand = [0,0]
        s.player_hand_sum = 0               # total value of player hand
        s.dealer_hand_sum = 0               # total value of dealer hand 
        s.split_hand_sum = 0                # total value of split hand (if applicable)
        s.round = 0                         # game round    
        s.final_reward = 0                  # unused atm

        s.player_hand[0] = s.__draw_card() 
        s.player_hand[1] = s.__draw_card() 
        # If there are 2 ACES, make one ACE = 1
        if (sum(s.player_hand) == 22):
            s.player_hand[0] = 1
        s.player_hand_sum = sum(s.player_hand)

        while (s.dealer_hand == [0,0]):
            s.dealer_hand[s.SHOWING] = s.__draw_card()
            s.dealer_hand[s.HIDDEN] = s.__draw_card()
            # If the dealer has 'blackjack', return card to deck and redraw 
            if (sum(s.dealer_hand) == 21):
                s.__return_card(s.dealer_hand[s.SHOWING])
                s.__return_card(s.dealer_hand[s.HIDDEN])
                s.dealer_hand = [0,0]                    
        # If there are 2 ACES, make hidden ACE = 1
        if (sum(s.dealer_hand) == 22):
            s.dealer_hand[s.HIDDEN] = 1
        s.dealer_hand_sum = sum(s.dealer_hand)

        state = s.build_state(s.player_hand)
        if (s.logs == True):
            print(f'State: {state}  Player Hand: {s.player_hand}  Player: {s.player_hand_sum}  Dealer showing: {s.dealer_hand[s.SHOWING]}  Reamining Deck: {s.deck}')
        return state

    def logs_on(s, logs):
        s.logs = logs

    def is_busted(s, hand_sum):
        reward = 0
        if (hand_sum > 21):
            reward = -s.bet
        return reward

    def do_action(s, move):
        state = None
        reward = 0        
        if (s.playing == True):
            s.round += 1
            state, reward = s.action[move](s)
            if (s.logs == True):
#                print(f'State: {state}  Reward: {reward}  Player: {s.player_hand_sum}  Player Hand: {s.player_hand}  Dealer: {s.dealer_hand_sum}  split: {s.split_hand_sum}  Split Hand: {s.split_hand}  Split Active= {s.split_active}  Split= {s.split}')
                print(f'State: {state}  Reward: {reward}  Player Hand: {s.player_hand}  Player: {s.player_hand_sum}  Dealer Showing: {s.dealer_hand[s.SHOWING]}  Player Hand: {s.player_hand}  Split: {s.split_hand_sum}  Split Hand: {s.split_hand}  Split Active= {s.split_active}  Split= {s.split}')
        elif (s.logs == True):
            print("No game in progress")
        return state, reward

    def __hit(s):
        reward = 0
        state = None
        card = s.__draw_card()
        if (s.split_active == True):
            s.split_hand.append(card)
            s.split_hand_sum += card
            reward = s.is_busted(s.split_hand_sum)
            if (reward < 0):
                if (card == 11):
                    reward = 0
                    s.split_hand_sum -= 10
                    state = s.build_state(s.split_hand)
                elif (s.split_hand[0] == 11):
                    reward = 0
                    s.split_hand[0] = 1
                    s.split_hand_sum -= 10
                    state = s.build_state(s.split_hand)
                elif (s.split_hand[1] == 11):
                    reward = 0
                    s.split_hand[1] = 1
                    s.split_hand_sum -= 10
                    state = s.build_state(s.split_hand)
                else:
                    state = s.build_state(s.player_hand)
                    s.split_active = False
                    reward = -s.bet
                    if (s.logs == True):
                        print(f"Split busted: {s.split_hand_sum}")

            else:
                state = s.build_state(s.split_hand)
        else:
            s.player_hand.append(card)
            s.player_hand_sum += card
            reward = s.is_busted(s.player_hand_sum)
            if (reward < 0):
                if (card == 11):
                    reward = 0
                    s.player_hand_sum -= 10
                    state = s.build_state(s.player_hand)
                elif (s.player_hand[0] == 11):
                    reward = 0
                    s.player_hand[0] = 1
                    s.player_hand_sum -= 10
                    state = s.build_state(s.player_hand)
                elif (s.player_hand[1] == 11):
                    reward = 0
                    s.player_hand[1] = 1
                    s.player_hand_sum -= 10
                    state = s.build_state(s.player_hand)
                else:
                    s.playing = False
                    if (s.logs == True):
                        print(f"Player busted: {s.player_hand_sum}")
                    if(s.split == True):
                        reward = -s.bet
                        reward = s.__stand()
            else:
                state = s.build_state(s.player_hand)
        return state, reward

    def __check_winner(s, hand_sum, hand_id):
        if (s.dealer_hand_sum > 21):
            if (s.logs == True):
                print(f"Dealer busted. {hand_id} won")
            reward = s.bet
        elif (s.dealer_hand_sum < s.player_hand_sum):
            if (s.logs == True):
                print(f"{hand_id}({hand_sum}) beat Dealer({s.dealer_hand_sum})")
            reward = s.bet
        elif (s.dealer_hand_sum > hand_sum):
            if (s.logs == True):
                print(f"Dealer({s.dealer_hand_sum}) beat {hand_id}({s.player_hand_sum})")
            reward = -s.bet
        elif (s.logs == True):
            print(f"{hand_id} Push ({hand_sum})")       
        return reward

    def __stand(s):
        state = None
        reward = 0
        if (s.split_active == True):
            state = s.build_state(s.player_hand)
            s.split_active = False
            s.split = True
            s.round = 1
            if (s.logs == True):
                print(f"Standing on Split hand({s.player_hand_sum}). Start Player hand")
        else:
            if (s.playing == True):
                if (s.logs == True):
                    print(f"Standing on Player hand")                    
                s.dealer_hand_sum = sum(s.dealer_hand)
                while (s.dealer_hand_sum < 17):
                    card = s.__draw_card()
                    s.dealer_hand_sum += card        
                reward += s.__check_winner(s.player_hand_sum, 'Player')
            if (s.split == True):
                reward += s.__check_winner(s.split_hand_sum, 'Split')
            s.playing = False                         
        return state, reward

    def __split(s):
        reward = 0
        if (s.round > 1):
            reward = -s.bet
            state = None
            s.playing = False
            if (s.logs == True):
                print("Can't split after round 1")
        elif (s.player_hand[0] != s.player_hand[1]):
            reward = -s.bet
            state = None
            s.playing = False
            if (s.logs == True):
                print("Cards must match to split")
        else:
            s.split_hand[0] = s.player_hand[1]
            s.split_hand[1] = s.__draw_card()
            s.player_hand[1] = s.__draw_card()
            s.player_hand_sum = sum(s.player_hand)
            s.split_hand_sum = sum(s.split_hand)
            s.split_active = True
            state = s.build_state(s.split_hand)
        return state, reward

    def __double_down(s):
        reward = 0
        state = None
        if (s.round > 1):
            reward = -s.bet
            s.playing = False
            if (s.logs == True):
                print("No game in progress")
        else:
            state, reward = s.__hit()
            if (reward == 0):
                state, reward = s.__stand()
        return state, reward

    def __draw_card(s):
        card = randrange(13)
        while (s.deck[card] < 1): 
            card = randrange(13)
        s.deck[card] -= 1
        card += 1
        if (card > 10):
            card = 10
        if (card == 1):
            card = 11
        if (s.logs == True):
            print(f'Drew: {card}')
        return card

    def __return_card(s, card):
        s.deck[card] += 1

    action = {
        0 : __hit,
        1 : __stand,
        2 : __split,
        3 : __double_down
    }


BET = 10
DECK_COUNT = 1

os.system('cls')
b = Blackjack(BET, DECK_COUNT)
b.logs_on(True)
b.start_hand()
reward = 0
while (reward == 0):
    print("1: Hit  2: Stand  3: Split  4: Double Down")
    action = input("Action: ")
    state, reward = b.do_action(int(action)-1)

# b.do_action(b.SPLIT)
# b.do_action(b.HIT)
# b.do_action(b.STAND)
# b.do_action(b.HIT)
# b.do_action(b.STAND)
# b.do_action(b.HIT)
# b.do_action(b.HIT)