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
        self.playing = False
        self.logs = False
        self.bet = bet
        self.master_deck = self.__build_deck(deck_count)
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = []
        self.player_hand_sum = 0
        self.split_hand_sum = 0
        self.round = 0
        self.split = False
        self.split_active = False
        self.final_reward = 0

    def __build_deck(s, deck_count):
        deck = []
        for card in range(1,10):
            deck.append(4*deck_count)
        for tens in range(4):
            deck.append(4*deck_count)
#        print(deck)
        return(deck)

    def start_hand(s):
        s.playing = True
        s.split_active = False 
        s.split = False
        s.deck = deepcopy(s.master_deck)
        s.player_hand = [0,0]
        s.dealer_hand = [0,0]
        s.split_hand = [0,0]
        s.player_hand_sum = 0
        s.dealer_hand_sum = 0
        s.split_hand_sum = 0

        s.player_hand[0] = s.__draw_card() 
        s.player_hand[1] = s.__draw_card() 

        while (s.dealer_hand == [0,0]):
            s.dealer_hand[s.SHOWING] = s.__draw_card()
            s.dealer_hand[s.HIDDEN] = s.__draw_card()
            if (s.dealer_hand[s.SHOWING] == 11 or s.dealer_hand[s.HIDDEN == 11]):
                if (sum(s.dealer_hand) == 21):
                    s.dealer_hand = [0,0]                    
        s.player_hand_sum = sum(s.player_hand)
        s.dealer_hand_sum = sum(s.dealer_hand)
        state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
        if (s.logs == True):
            print(f'State: {state}  Dealer: {s.dealer_hand}  Reamining Deck: {s.deck}')
        return state

    def logs_on(s, logs):
        s.logs = logs

    def do_action(s, move):
        state = None
        reward = 0        
        if (s.playing == True):
            s.round += 1
            state, reward = s.action[move](s)
            if (s.logs == True):
                print(f'State: {state}  Reward: {reward}  Player: {s.player_hand_sum}  Player Hand: {s.player_hand}  Dealer: {s.dealer_hand_sum}  split: {s.split_hand_sum}  Split Hand: {s.split_hand}  Split Active= {s.split_active}  Split= {s.split}')
        elif (s.logs == True):
            print("No game in progress")
        return state, reward

    def is_busted(s, hand_sum):
        reward = 0
        if (hand_sum > 21):
            if (s.logs == True):
                print(f"Busted: {hand_sum}")
            reward = -s.bet
        return reward

#    def __dealer_play(s):

    def __hit(s):
        reward = 0
        state = None
        card = s.__draw_card()
        if (s.split_active == True):
            s.split_hand_sum += card
            reward = s.is_busted(s.split_hand_sum)
            if (reward < 0):
                if (card == 11):
                    reward = 0
                    s.split_hand_sum -= 10
                    state = tuple([tuple(s.split_hand), s.split_hand_sum, s.dealer_hand[s.SHOWING]]) 
                elif (s.split_hand[0] == 11):
                    reward = 0
                    s.split_hand[0] = 1
                    s.split_hand_sum -= 10
                    state = tuple([tuple(s.split_hand), s.split_hand_sum, s.dealer_hand[s.SHOWING]])                    
                elif (s.split_hand[1] == 11):
                    reward = 0
                    s.split_hand[1] = 1
                    s.split_hand_sum -= 10
                    state = tuple([tuple(s.split_hand), s.split_hand_sum, s.dealer_hand[s.SHOWING]])                    
                else:
                    state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
                    s.split_active = False
            else:
                state = tuple([tuple(s.split_hand), s.split_hand_sum, s.dealer_hand[s.SHOWING]])                    
        else:
            s.player_hand_sum += card
            reward = s.is_busted(s.player_hand_sum)
            if (reward < 0):
                if (card == 11):
                    reward = 0
                    s.player_hand_sum -= 10
                    state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
                elif (s.player_hand[0] == 11):
                    reward = 0
                    s.player_hand[0] = 1
                    s.player_hand_sum -= 10
                    state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
                elif (s.player_hand[1] == 11):
                    reward = 0
                    s.player_hand[1] = 1
                    s.player_hand_sum -= 10
                    state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
                else:
                    s.playing = False
                    if(s.split == True):
                        reward = -s.bet
                        reward = s.__stand()
            else:
                state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
        return state, reward

    def __stand(s):
        state = None
        reward = 0
        if (s.split_active == True):
            state = tuple([tuple(s.player_hand), s.player_hand_sum, s.dealer_hand[s.SHOWING]])
            s.split_active = False
            s.split = True
            s.round = 1
            if (s.logs == True):
                print("Standing on split hand. Start main hand")
        else:
            if (s.playing == True):
                if (s.logs == True):
                    print("Standing on main hand.")                    
                s.dealer_hand_sum = sum(s.dealer_hand)
                while (s.dealer_hand_sum < 17):
                    card = s.__draw_card()
                    s.dealer_hand_sum += card        
                if (s.dealer_hand_sum > 21):
                    if (s.logs == True):
                        print("Dealer busted. Player won")
                    reward = s.bet
                elif (s.dealer_hand_sum < s.player_hand_sum):
                    if (s.logs == True):
                        print("Player beat Dealer")
                    reward = s.bet
                elif (s.dealer_hand_sum > s.player_hand_sum):
                    if (s.logs == True):
                        print("Dealer beat Player")
                    reward = -s.bet
            if (s.split == True):
                if (s.dealer_hand_sum > 21):
                    if (s.logs == True):
                        print("Dealer busted. Split won")
                    reward += s.bet
                elif (s.dealer_hand_sum < s.split_hand_sum):
                    if (s.logs == True):
                        print("Split beat Dealer")
                    reward += s.bet
                elif (s.dealer_hand_sum > s.split_hand_sum):
                    if (s.logs == True):
                        print("Dealer beat Split")
                    reward += -s.bet           
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
            state = tuple([tuple(s.split_hand), s.split_hand_sum, s.dealer_hand[s.SHOWING]])
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
b.do_action(b.SPLIT)
b.do_action(b.HIT)
b.do_action(b.STAND)
b.do_action(b.HIT)
b.do_action(b.STAND)
b.do_action(b.HIT)
b.do_action(b.HIT)