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
        self.hands = [[0,0],[0,0],[0,0]]        # Stores the hands of player, split, and dealer
        self.hand_sums = [0,0,0]                # Stores the sums of player, split, and dealer hands
        self.player_lost = False                
        self.split_lost = False
        self.player_won = False
        self.split_won = False
        self.dealer_lost = False
        self.round = 0                          # game round    
        self.final_reward = 0                   # final reward
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
        s.hand_sums = [0,0,0]               # Stores the sums of player, split, and dealer hands
        s.player_lost = False
        s.split_lost = False
        s.player_won = False
        s.split_won = False
        s.dealer_lost = False
        s.round = 0                         # game round    
        s.final_reward = 0                  # unused atm

        s.hands[s.PLAYER_HAND][0] = s.__draw_card() 
        s.hands[s.PLAYER_HAND][1] = s.__draw_card() 
        # If there are 2 ACES, make one ACE = 1
        if (sum(s.hands[s.PLAYER_HAND]) == 22):
            s.hands[s.PLAYER_HAND][0] = 1
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
        s.hand_sums[s.DEALER_HAND] = sum(s.hands[s.DEALER_HAND])

        state = s.build_state(s.hands[s.PLAYER_HAND])
        if (s.logs == True):
            print(f'State: {state}  Player Hand: {s.hands[s.PLAYER_HAND]}  Player: {s.hand_sums[s.PLAYER_HAND]}  Dealer showing: {s.hands[s.DEALER_HAND][s.SHOWING]}  Reamining Deck: {s.deck}')
        return state

    def do_action(s, move):
        state = None
        if (s.playing == True):
            s.round += 1
            s.action[move](s)
            if (s.split_active == True):
                state = s.build_state(s.hands[s.SPLIT_HAND])
            elif (s.playing == True):
                state = s.build_state(s.hands[s.PLAYER_HAND])
            if (s.playing == False):
                if (s.split_lost == True):
                    s.final_reward += -s.bet
                elif (s.split_won):
                    s.final_reward += s.bet
                if (s.player_lost == True):
                    s.final_reward += -s.bet
                elif (s.player_won):
                    s.final_reward += s.bet
            if (s.logs == True):
#                print(f'State: {state}  Reward: {s.final_reward}  Player Hand: {s.hands[s.PLAYER_HAND]}  Player: {s.hand_sums[s.PLAYER_HAND]}  Dealer: {s.hand_sums[s.DEALER_HAND]}  Dealer Hand: {s.hands[s.DEALER_HAND]}  Split: {s.hand_sums[s.SPLIT_HAND]}  Split Hand: {s.hands[s.SPLIT_HAND]}  Split Active={s.split_active}  Split={s.split}  Playing={s.playing}  Player Lost={s.player_lost}  Split Lost={s.split_lost}')
                print(f'State: {state}  Reward: {s.final_reward}  Dealer Showing: {s.hands[s.DEALER_HAND][s.SHOWING]}  Player Hand: {s.hands[s.PLAYER_HAND]}  Player: {s.hand_sums[s.PLAYER_HAND]}  Split: {s.hand_sums[s.SPLIT_HAND]}  Split Hand: {s.hands[s.SPLIT_HAND]}  Split Active={s.split_active}  Split={s.split}  Playing={s.playing}  Player Lost={s.player_lost}  Split Lost={s.split_lost}')
        elif (s.logs == True):
            print("No game in progress")
        return state, s.final_reward

    def __hit(s):
        card = s.__draw_card()
        if (s.split_active == True):
            s.hands[s.SPLIT_HAND].append(card)
            s.hand_sums[s.SPLIT_HAND] += card
            s.split_lost = s.__is_busted(s.hand_sums[s.SPLIT_HAND])
            if (s.split_lost):
                s.split_lost = s.__check_aces(s.SPLIT_HAND)
                if (s.split_lost == True):
                    s.split_active = False
                if (s.logs == True):
                    print(f"Split busted: {s.hand_sums[s.SPLIT_HAND]}")
        else:
            s.hands[s.PLAYER_HAND].append(card)
            s.hand_sums[s.PLAYER_HAND] += card
            s.player_lost = s.__is_busted(s.hand_sums[s.PLAYER_HAND])
            if (s.player_lost == True):
                s.player_lost = s.__check_aces(s.PLAYER_HAND)
                if (s.player_lost == True):
                    s.playing = False
                    if (s.logs == True):
                        print(f"Player busted: {s.hand_sums[s.PLAYER_HAND]}")    
                    if(s.split == True):
                        s.__dealer_play()

    def __is_busted(s, hand_sum):
        busted = False
        if (hand_sum > 21):
            busted = True
        return busted

    # Determine if there is an Ace in hand_id's hand and change it from 11 to 1
    def __check_aces(s, hand_id):
        busted = True
        for card in range(len(s.hands[hand_id])):
            if (s.hands[hand_id][card] == 11):
                s.hands[hand_id][card] = 1
                s.hand_sums[hand_id] -= 10
                busted = s.__is_busted(s.hand_sums[hand_id])
                break
        return busted

    def __stand(s):
        if (s.split_active == True):
            s.split_active = False
            s.split = True
            if (s.logs == True):
                print(f"Standing on Split hand({s.hand_sums[s.SPLIT_HAND]}). Start Player hand")
        elif (s.player_lost != True):
            if (s.logs == True):
                print(f"Standing on Player hand")                    
            s.playing = False                         
        if (s.playing == False):
            s.__dealer_play()

    def __split(s):
        if (s.round > 1):
            if (s.split_active == True):
                s.split_active = False
                s.split_lost = True
                if (s.logs == True):
                    print("Can't split a split")
            else:
                s.player_lost = True    
                s.playing = False
                if (s.logs == True):
                    print("Can't split after round 1")
        elif (s.hands[s.PLAYER_HAND][0] != s.hands[s.PLAYER_HAND][1]):
            if (s.split_active == True):
                s.split_active = False
                s.split_lost = True
                if (s.logs == True):
                    print("Can't split a split")
            else:
                s.player_lost = True    
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

    def __double_down(s):
        if (s.round > 1):
            s.player_lost = True    
            s.playing = False
            if (s.logs == True):
                print("No game in progress")
        else:
            s.__hit()
            if (s.player_lost != True):
                s.__stand()

    def __dealer_play(s):
        s.hand_sums[s.DEALER_HAND] = sum(s.hands[s.DEALER_HAND])
        while (s.hand_sums[s.DEALER_HAND] < 17):
            card = s.__draw_card()
            s.hands[s.DEALER_HAND].append(card)
            s.hand_sums[s.DEALER_HAND] += card
            s.dealer_lost = s.__is_busted(s.hand_sums[s.DEALER_HAND])
            if (s.dealer_lost == True):
                s.dealer_lost = s.__check_aces(s.DEALER_HAND)
        if (s.player_lost != True):
            s.player_won += s.__check_winner(s.hand_sums[s.PLAYER_HAND], 'Player')
        if (s.split == True):
            s.split_won += s.__check_winner(s.hand_sums[s.SPLIT_HAND], 'Split')                         

    def __check_winner(s, hand_sum, hand_id):
        player_won = False    
        if (s.dealer_lost == True):
            if (s.logs == True):
                print(f"Dealer busted. {hand_id} won")
            player_won = True
        elif (s.hand_sums[s.DEALER_HAND] < s.hand_sums[s.PLAYER_HAND]):
            if (s.logs == True):
                print(f"{hand_id}({hand_sum}) beat Dealer({s.hand_sums[s.DEALER_HAND]})")
            player_won = True
        elif (s.hand_sums[s.DEALER_HAND] > hand_sum):
            if (s.logs == True):
                print(f"Dealer({s.hand_sums[s.DEALER_HAND]}) beat {hand_id}({s.hand_sums[s.PLAYER_HAND]})")
            s.player_lost = True
        elif (s.logs == True):
            print(f"{hand_id} Push ({hand_sum})")       
        return player_won

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
#        if (s.logs == True):
#            print(f'Drew: {card}')
        return card

    def __return_card(s, card):
        s.deck[card] += 1

    def logs_on(s, logs):
        s.logs = logs

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