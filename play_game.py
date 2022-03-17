from blackjack_player import Blackjack
from blackjackChrom import chromosome
from q_table import Q_Table

GA_FILE = 'best-chromosome.txt'
Q_FILE = 'q-table.txt'
NUM_HANDS = 100

class GA_player:
    def __init__(self):
        self.read_in_strategy(GA_FILE)

    def read_in_strategy(self, filename):
        file = open(filename, 'r')
        line = file.readline()
        self.chromosome = chromosome(line)

    def play_hands(self, num_hands):
        final_reward = 2000
        game = Blackjack(10,1)
        geneStr = list(self.chromosome.string)
        for _ in range(num_hands):
            state = game.start_hand()
            while(state != None):
                gene = self.chromosome.action_map[state]
                action = int(geneStr[gene]) 
                state, reward = game.do_action(action)

            #decrease by amount lost only
            if(reward[0] > 0):
                final_reward += reward[0] 
        return final_reward


class Q_player:
    def __init__(self):
        self.strategy = Q_Table()
        self.strategy.read_in(Q_FILE) 

    def play_hands(self, num_hands):
        final_reward = 2000
        game = Blackjack(10,1)

        for _ in range(num_hands):
            state = game.start_hand()
            self.strategy.starting_state(state)
            while(state != None):
                action = self.strategy.choose_action()
                state, reward = game.do_action(action)

            #decrease by amount lost only
            if(reward[0] > 0):
                final_reward += reward[0] 
        return final_reward




def main():
    #game = Blackjack(10,1)
    #state = game.start_hand()

    ga_player = GA_player()
    q_player = Q_player()

    ga_reward = ga_player.play_hands(NUM_HANDS)
    q_reward = q_player.play_hands(NUM_HANDS)

    print("The GA player's final reward amount:", ga_reward)
    print("The Q-learning player's final reward amount:", q_reward)



if __name__ == '__main__':
    main()