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
str5  = "hhhhhhhhhh"
str6  = "hhhhhhhhhh"
str7  = "hhhhhhhhhh"
str8  = "hhhddhhhhh"
str9  = "dddddhhhhh"
str10 = "ddddddddhh"
str11 = "dddddddddd"
str12 = "hhssshhhhh"
str13 = "ssssshhhhh"
str14 = "ssssshhhhh"
str15 = "ssssshhhhh"
str16 = "ssssshhhhh"
str17 = "ssssssssss"
str18 = "ssssssssss"
str19 = "ssssssssss"
str20 = "ssssssssss"
strA2 = "hhdddhhhhh"
strA3 = "hhdddhhhhh"
strA4 = "hhdddhhhhh"
strA5 = "hhdddhhhhh"
strA6 = "dddddhhhhh"
strA7 = "sddddsshhs"
strA8 = "ssssdsssss"
strA9 = "ssssssssss"
str22 = "hppppphhhh"
str33 = "hhpppphhhh"
str44 = "hhhddhhhhh"
str55 = "ddddddddhh"
str66 = "ppppphhhhh"
str77 = "pppppphhsh"
str88 = "pppppppppp"
str99 = "pppppsppss"
str00 = "ssssssssss"
BASICSTRATEGY = str5+str6+str7+str8+str9+str10+str11+str12+str13+str14+str15+str16+str17+str18+str19+str20+strA2+strA3+strA4+strA5+strA6+strA7+strA8+strA9+str22+str33+str44+str55+str66+str77+str88+str99+str00


class chromosome(object):

    def __init__(self, init_string=None):
        self.size = 330
        self.fitness = -1
        if init_string:
            self.string = init_string
        else:
            self.string = self.genRandString()

    def genRandString(self):
        chars = ['h', 's', 'd', 'p']
        randStr = ""
        for _ in range(self.size):
            randStr += choice(chars)
        return randStr

    def getFitness(self):
        if self.fitness < 0:
            return self.size-self.countDiff(BASICSTRATEGY)
        else:
            return self.fitness

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
                print("ovjects not same size")
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
        return (chromosome(str1), chromosome(str2))

    def mutate(self):
        chars = ['h', 's', 'd', 'p']
        edStr = list(self.string)
        edStr[randint(0,self.size-1)] = choice(chars)
        self.string = "".join(edStr)
        

    

