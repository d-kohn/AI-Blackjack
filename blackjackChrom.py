from unittest import findTestCases
from blackjack import Blackjack
"""
blackJackChrom.py -- 
A class for representing blackjack basic strategy as a chromosome in a
genetic algorithm. 
The normal blackjack basic strategy chart is a 2 dimensional grid in which 
the rows corrospond to different sorts of hands the players might have, 
the columns corrospond to the cards that the dealer might be showing, and
the value in the chart at a given position proscribes the action that the
player should take given their hand and the dealer's hand. 
The chromosomes are essentially this chart laid out in row major order. 
There are 10 different cards (2, 3, 4, 5, 6, 7, 8, 9, 10, A) so there are
10 different columns to describe the dealer's face up card. In general we 
do not care about the exact hand a player has but rather the total of the
player's hand. The only specific hands we need to enumerate are pairs
(because often the right move is to split) and "soft" hands - those that 
contain aces (because ace's can take two different values). 
The chart, then, looks something like this:
     2  3  4  5  6  7  8  9  10  A
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
A2
A3
A4
A5
A6
A7
A8
A9
11
22
33
44
55
66
77
88
99
10/10
AA

Note that hand totals start at five (any three's are covered in the aces
section and any 4's by aces or pairs) and the A10 hand is omitted (for
obvious reasons). In total there are 35 rows, each of which has 10 columns
and so the chromosome has 350 slots. The four possible actions that a 
player can take are Hit "h", Stay "s", Double Down "d", and Split "p". So
every chromosome generated will be 350 characters long and the characters
will be from the set {h, s, d, p}
"""

from random import choice, randint

#Basic strategy chart -used as reference and naive fitness
# Round 1
str4  = "0000000000"
str5  = "0000000000"
str6  = "0000000000"
str7  = "0000000000"
str8  = "0002200000"
str9  = "2222200000"
str10 = "2222222200"
str11 = "2222222222"
str12 = "0011100000"
str13 = "1111100000"
str14 = "1111100000"
str15 = "1111100000"
str16 = "1111100000"
str17 = "1111111111"
str18 = "1111111111"
str19 = "1111111111"
str20 = "1111111111"
str21 = "1111111111"
strAA = "3333333333"
strA2 = "0022200000"
strA3 = "0022200000"
strA4 = "0022200000"
strA5 = "0022200000"
strA6 = "2222200000"
strA7 = "1222211001"
strA8 = "1111211111"
strA9 = "1111111111"
str22 = "0333330000"
str33 = "0033330000"
str44 = "0002200000"
str55 = "2222222200"
str66 = "3333300000"
str77 = "3333330010"
str88 = "3333333333"
str99 = "3333313311"
str00 = "1111111111"

# Round 2+
str4_2  = "0000000000"
str5_2  = "0000000000"
str6_2  = "0000000000"
str7_2  = "0000000000"
str8_2  = "0000000000"
str9_2  = "0000000000"
str10_2 = "0000000000"
str11_2 = "0000000000"
str12_2 = "0011100000"
str13_2 = "1111100000"
str14_2 = "1111100000"
str15_2 = "1111100000"
str16_2 = "1111100000"
str17_2 = "1111111111"
str18_2 = "1111111111"
str19_2 = "1111111111"
str20_2 = "1111111111"
str21_2 = "1111111111"
strAA_2 = "0000000000"
strA2_2 = "0000000000"
strA3_2 = "0000000000"
strA4_2 = "0000000000"
strA5_2 = "0000000000"
strA6_2 = "0001000000"
strA7_2 = "1100011001"
strA8_2 = "1111111111"
strA9_2 = "1111111111"
str22_2 = "0000000000"
str33_2 = "0000000000"
str44_2 = "0000000000"
str55_2 = "0000000000"
str66_2 = "0000000000"
str77_2 = "0000000000"
str88_2 = "0000000000"
str99_2 = "0000000000"
str00_2 = "0000000000"
BASICSTRATEGY = str4+str5+str6+str7+str8+str9+str10+str11+str12+str13+str14+str15+str16+str17+str18+str19+str20+str21+strAA+strA2+strA3+strA4+strA5+strA6+strA7+strA8+strA9+str22+str33+str44+str55+str66+str77+str88+str99+str00
BASICSTRATEGY += str4_2+str5_2+str6_2+str7_2+str8_2+str9_2+str10_2+str11_2+str12_2+str13_2+str14_2+str15_2+str16_2+str17_2+str18_2+str19_2+str20_2+str21_2+strAA_2+strA2_2+strA3_2+strA4_2+strA5_2+strA6_2+strA7_2+strA8_2+strA9_2+str22_2+str33_2+str44_2+str55_2+str66_2+str77_2+str88_2+str99_2+str00_2

class chromosome(object):
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    SPLIT = 3

    action_string = {
        0 : 'HIT',
        1 : 'STAND',
        2 : 'DBL DWN',
        3 : 'SPLIT'
    }
 
    action_map = {} # Maps blackjack state to a gene # in the chromosome string

    def __init__(self, init_string=None):
        self.logs = False
        self.size = 720
        self.fitness = 0
        if init_string:
            self.string = init_string
            if(self.logs == True):
                print(f"Chromosome length= {len(self.string)}")
        else:
            self.string = self.genRandString()
        self.build_action_map()
    
    def genRandString(s):
        actions = [s.HIT, s.STAND, s.DOUBLE_DOWN, s.SPLIT]
        randStr = ""
        for _ in range(s.size):
            randStr += str(choice(actions)) #BUG fix: prior version created empty elements that did not cast to int in getFitness
        return randStr

    # Map game states to a chromosome string index
    def build_action_map(self):
        gene = 0  # Gene position in chromosome string
        for round in range(1, 3):
            for hand_state in range(4,40):
                for dealer_showing_card in range (2, 12):               
                    state = (hand_state, dealer_showing_card, round)
                    self.action_map[state] = gene
                    gene += 1
        if (self.logs == True):
            print(f'Total genes: {gene}')

    def getFitness(self, hands_to_play):
        game = Blackjack(10,1)
        fitness = 0
        edStr = list(self.string)
        for _ in range(hands_to_play):
            state = game.start_hand()
            # Loop until player wins/loses
            while (state != None):
                # Using the current game state, get the gene # from the action map                  
                gene = self.action_map[state]
                # Get the next action to play from the chromosome string using the gene index
                action = int(edStr[gene]) #BUG: nothing to cast if the item at index is ' '
                if (self.logs == True):
                    print(f'Gene: {gene}  Action: {action}')
                    print(f'State: {state}  Next action {self.action_string[action]}')
                # Play action, get next game state or reward list
                state, reward = game.do_action(action)
            fitness += reward[0] 
            if (self.logs == True):
                print (f'Current fitness= {fitness}  Latest Reward= {reward}')
        return fitness

    def countDiff(self, other):
        count = 0
        if isinstance(other, str):
            if self.size != len(other):
                print("objects not same size")
                return None
            for i in range(self.size):
                if self.string[i] != other[i]:
                    count += 1
        elif isinstance(other, chromosome):
            if self.size != other.size:
                print("objects not same size")
                return None
            for i in range(self.size):
                if self.string[i] != other.string[i]:
                    count += 1
        return count
            
    def __str__(self):
        return self.string

    def __eq__(self, other):
        if self.string == other.string:
            return True
        else:
            return False

    def crossover(self, other):
        if not isinstance(other, chromosome):
            print("Tried to crossover non-chromosome: ",end="")
            print(other)
            return None
        crossInd = randint(0, self.size-1)
        str1 = self.string[:crossInd]+other.string[crossInd:]
        str2 = other.string[:crossInd]+self.string[crossInd:]
        return (self.mutate(chromosome(str1)), self.mutate(chromosome(str2)))

    def mutate(s):
        actions = [s.HIT, s.STAND, s.DOUBLE_DOWN, s.SPLIT]
        edStr = list(s.string)
        edStr[randint(0,s.size-1)] = choice(actions)
        s.string = "".join(edStr)
        
    def output_action_table(s, file):
        with open(file, "w") as f:
            for round in range(1,3):
                f.write(f'Round {round}\n')
                for hand_state in range(4, 40):
                    for dealer in range(2, 12):
                        key = tuple([hand_state,dealer,round])
                        gene = s.action_map[key]
                        if (s.logs == True):
                           print(f'Gene: {gene}  Key: {key}')
                        action = (list(s.string))[gene]
                        f.write(f'{s.action_string[int(action)]},')
                    f.write('\n')
        f.close()

# chrome = chromosome(BASICSTRATEGY)
# total_scores = 0
# for _ in range(100):
#     fitness = chrome.getFitness(500)
#     total_scores += fitness
#     print(f'Fitness: {fitness}')
# print(f'Average fitness over 100 episodes (500 hands each): {total_scores/100}')
# chrome.output_action_table("actions_ga.csv")

