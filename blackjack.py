from copy import deepcopy
from random import randrange
import os

class Blackjack():
    SHOWING = 0
    HIDDEN = 1

    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    SPLIT = 3

    PLAYER_HAND = 0
    SPLIT_HAND = 1
    DEALER_HAND = 2

    id = {
        0 : 'Player',
        1 : 'Split',
        2 : 'Dealer'
    }

    def __init__(self, bet, deck_count):
        # Master deck copied to make a game deck
        self.master_deck = self.__build_deck(deck_count)
        self.playing = False                    # game in progress?
        self.logs = False                       # display logs?
        self.bet = bet                          # possible reward for winning/losing                          
        self.deck = []                          # current game deck
        self.hands = [[0,0],[0,0],[0,0]]
        self.hand_sums = [0,0,0]                   # Stores the sums of player, split, and dealer hands
        self.player_busted = False
        self.split_busted = False
        self.dealer_busted = False
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
            # If card one is an Ace, make the state 10 higher than its total
            for i in range(len(hand)):
                if (hand[i] == 11):
                    hand_sum += 10
                    break
            # Otherwise, the state = the sum of the cards
            else:
                hand_sum = sum(hand)
        return tuple([hand_sum, s.hands[s.DEALER_HAND][s.SHOWING]])

    def start_hand(s):
        s.playing = True
        s.split_active = False 
        s.split = False
        s.deck = deepcopy(s.master_deck)
        s.hands = [[0,0],[0,0],[0,0]]
        s.hand_sums = [0,0,0]                   # Stores the sums of player, split, and dealer hands
        s.player_busted = False
        s.split_busted = False
        s.dealer_busted = False
        s.round = 0                         # game round    
        s.final_reward = 0                  # unused atm

        s.hands[s.PLAYER_HAND][0] = s.__draw_card() 
        s.hands[s.PLAYER_HAND][1] = s.__draw_card() 
        # If there are 2 ACES, make one ACE = 1
        if (sum(s.hands[s.PLAYER_HAND]) == 22):
            s.hands[s.PLAYER_HAND][0] = 1
#        s.player_hand_sum = sum(s.player_hand)
        s.hand_sums[s.PLAYER_HAND] = sum(s.hands[s.PLAYER_HAND])
        while (s.hands[s.DEALER_HAND] == [0,0]):
            s.hands[s.DEALER_HAND][s.SHOWING] = s.__draw_card()
            s.hands[s.DEALER_HAND][s.HIDDEN] = s.__draw_card()
            # If the dealer has 'blackjack', return card to deck and redraw 
            if (sum(s.hands[s.DEALER_HAND]) == 21):
                s.__return_card(s.hands[s.DEALER_HAND][s.SHOWING])
                s.__return_card(s.hands[s.DEALER_HAND][s.HIDDEN])
                s.hands[s.DEALER_HAND] = [0,0]                    
        # If there are 2 ACES, make hidden ACE = 1
        if (sum(s.hands[s.DEALER_HAND]) == 22):
            s.hands[s.DEALER_HAND][s.HIDDEN] = 1
#        s.dealer_hand_sum = sum(s.dealer_hand)
        s.hand_sums[s.DEALER_HAND] = sum(s.hands[s.DEALER_HAND])

        state = s.build_state(s.hands[s.PLAYER_HAND])
        if (s.logs == True):
            print(f'State: {state}  Player Hand: {s.hands[s.PLAYER_HAND]}  Player: {s.hand_sums[s.PLAYER_HAND]}  Dealer showing: {s.hands[s.DEALER_HAND][s.SHOWING]}  Reamining Deck: {s.deck}')
        return state

    def logs_on(s, logs):
        s.logs = logs

    def is_busted(s, hand_sum):
        busted = False
        if (hand_sum > 21):
            busted = True
        return busted

    def do_action(s, move):
        state = None
        reward = 0        
        if (s.playing == True):
            s.round += 1
            state, reward = s.action[move](s)
            if (s.logs == True):
#                print(f'State: {state}  Reward: {reward}  Player: {s.player_hand_sum}  Player Hand: {s.player_hand}  Dealer: {s.dealer_hand_sum}  split: {s.split_hand_sum}  Split Hand: {s.split_hand}  Split Active= {s.split_active}  Split= {s.split}')
                print(f'State: {state}  Reward: {reward}  Player Hand: {s.hands[s.PLAYER_HAND]}  Player: {s.hand_sums[s.PLAYER_HAND]}  Dealer Showing: {s.hands[s.DEALER_HAND][s.SHOWING]}  Split: {s.hand_sums[s.SPLIT_HAND]}  Split Hand: {s.hands[s.SPLIT_HAND]}  Split Active= {s.split_active}  Split= {s.split}')
        elif (s.logs == True):
            print("No game in progress")
        return state, reward

    def __check_aces(s, reward, hand_id, id):
        state = None
        for card in range(len(s.hands[hand_id])):
            if (s.hands[hand_id][card] == 11):
                s.hands[hand_id][card] = 1
                s.hand_sums[hand_id] -= 10
                reward = s.is_busted(s.hand_sums[hand_id])
                if (reward == 0):
                    state = s.build_state(s.hands[hand_id])
                break
        if (reward < 0):
            if (hand_id == s.SPLIT_HAND):
                s.split_busted = True
            elif (hand_id == s.PLAYER_HAND):
                s.playing = False
                s.player_busted = True
                if(s.split == True):
                    state, reward = s.__stand()
            if (s.logs == True):
                print(f"{id} busted: {s.hand_sums[hand_id]}")
        return state, reward

    def __hit(s):
        reward = 0
        state = None
        card = s.__draw_card()
        if (s.split_active == True):
            s.hands[s.SPLIT_HAND].append(card)
            s.hand_sums[s.SPLIT_HAND] += card
            s.split_busted = s.is_busted(s.hand_sums[s.SPLIT_HAND])
            if (s.split_busted):
                s.split_busted = s.__check_aces(reward, s.SPLIT_HAND, 'Split')
                if (s.split_busted == True):
                    state = s.build_state(s.hands[s.PLAYER_HAND])
                    s.split_active = False
            else:
                state = s.build_state(s.hands[s.SPLIT_HAND])
        else:
            s.hands[s.PLAYER_HAND].append(card)
            s.hand_sums[s.PLAYER_HAND] += card
            s.player_busted = s.is_busted(s.hand_sums[s.PLAYER_HAND])
            if (s.player_busted):
                s.player_busted = s.__check_aces(reward, s.PLAYER_HAND, 'Player')
            else:
                state = s.build_state(s.hands[s.PLAYER_HAND])
        return state, reward

    def __check_winner(s, hand_sum, hand_id):
        if (s.hand_sums[s.DEALER_HAND] > 21):
            if (s.logs == True):
                print(f"Dealer busted. {hand_id} won")
            reward = s.bet
        elif (s.hand_sums[s.DEALER_HAND] < s.hand_sums[s.PLAYER_HAND]):
            if (s.logs == True):
                print(f"{hand_id}({hand_sum}) beat Dealer({s.hand_sums[s.DEALER_HAND]})")
            reward = s.bet
        elif (s.hand_sums[s.DEALER_HAND] > hand_sum):
            if (s.logs == True):
                print(f"Dealer({s.hand_sums[s.DEALER_HAND]}) beat {hand_id}({s.hand_sums[s.PLAYER_HAND]})")
            reward = -s.bet
        elif (s.logs == True):
            print(f"{hand_id} Push ({hand_sum})")       
        return reward

# Need to check dealer aces
    def __stand(s):
        state = None
        reward = 0
        if (s.split_active == True):
            state = s.build_state(s.hands[s.PLAYER_HAND])
            s.split_active = False
            s.split = True
            s.round = 1
            if (s.logs == True):
                print(f"Standing on Split hand({s.hand_sums[s.PLAYER_HAND]}). Start Player hand")
        else:
            if (s.playing == True):
                if (s.logs == True):
                    print(f"Standing on Player hand")                    
                s.hand_sums[s.DEALER_HAND] = sum(s.hands[s.DEALER_HAND])
                while (s.hand_sums[s.DEALER_HAND] < 17):
                    card = s.__draw_card()
                    s.hand_sums[s.DEALER_HAND] += card        
                reward += s.__check_winner(s.hand_sums[s.PLAYER_HAND], 'Player')
        if (s.split == True):
            reward += s.__check_winner(s.hand_sums[s.SPLIT_HAND], 'Split')
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
        elif (s.hands[s.PLAYER_HAND][0] != s.hands[s.PLAYER_HAND][1]):
            reward = -s.bet
            state = None
            s.playing = False
            if (s.logs == True):
                print("Cards must match to split")
        else:
            s.hands[s.SPLIT_HAND][0] = s.hands[s.PLAYER_HAND][1]
            s.hands[s.SPLIT_HAND][1] = s.__draw_card()
            s.hands[s.PLAYER_HAND][1] = s.__draw_card()
            s.hand_sums[s.PLAYER_HAND] = sum(s.hands[s.PLAYER_HAND])
            s.hand_sums[s.SPLIT_HAND] = sum(s.hands[s.SPLIT_HAND])
            s.split_active = True
            state = s.build_state(s.hands[s.SPLIT_HAND])
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
        2 : __double_down,
        3 : __split
    }

BET = 10
DECK_COUNT = 1

os.system('cls')
b = Blackjack(BET, DECK_COUNT)
b.logs_on(True)
b.start_hand()
reward = 0
while (reward == 0):
    print("1: Hit  2: Stand 3: Double Down 4: Split")
    action = input("Action: ")
    state, reward = b.do_action(int(action)-1)

# b.do_action(b.SPLIT)
# b.do_action(b.HIT)
# b.do_action(b.STAND)
# b.do_action(b.HIT)
# b.do_action(b.STAND)
# b.do_action(b.HIT)
# b.do_action(b.HIT)