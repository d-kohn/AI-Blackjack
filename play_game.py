from blackjack_player import Blackjack
from blackjackChrom import chromosome
from q_table import Q_Table
from matplotlib import pyplot as plt

GA_FILE = 'best-chromosome.txt'
Q_FILE = 'q-table.txt'
NUM_HANDS = 200
NUM_EPISODES = 1000

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
            if(reward[0] < 0):
                final_reward += reward[0] 
        return final_reward


class Q_player:
    def __init__(self):
        self.strategy = Q_Table(4)
        self.strategy.read_in(Q_FILE) 

    def play_hands(self, num_hands):
        final_reward = 2000
        game = Blackjack(10,1)

        for _ in range(num_hands):
            state = game.start_hand()
            self.strategy.set_state(state)
            while(state != None):
                action = self.strategy.choose_action()
                state, reward = game.do_action(action)
                self.strategy.set_state(state)

            #decrease by amount lost only
            if(reward[0] < 0):
                final_reward += reward[0] 
        return final_reward

class Graph:
    def __init__(self):
        self.x_limit = NUM_EPISODES
        self.y_limit = 2000
        self.ys = [] #ga
        self.zs = [] #q
        self.xs = [] #episode

    def add_scores(self, ga_score, q_score, i):
        self.ys.append(ga_score)
        self.zs.append(q_score)
        self.xs.append(i)

    def show_plot(self):
        plt.plot(self.xs, self.ys, 'c')
        plt.plot(self.xs, self.zs, 'r')
        plt.xlim([0, self.x_limit])
        plt.ylim([0, self.y_limit])
        ga_ave = round(sum(self.ys)/max(self.xs))
        q_ave = round(sum(self.zs)/max(self.xs))
        ave_string = "GA average:" + str(ga_ave) + " Q average:" + str(q_ave)
        plt.suptitle(ave_string)
        plt.xlabel('Episodes')
        plt.ylabel('Reward')
        plt.savefig("GA vs Q Players")
        plt.show()


def main():
    #chr_file = "GA_strat_sheet.csv"
    graph = Graph()

    for i in range(NUM_EPISODES):
        ga_player = GA_player()
        q_player = Q_player()

        ga_reward = ga_player.play_hands(NUM_HANDS)
        q_reward = q_player.play_hands(NUM_HANDS)
        #print("The GA player's final reward amount:", ga_reward)
        #print("The Q-learning player's final reward amount:", q_reward)
    
        graph.add_scores(ga_reward, q_reward, i)

    graph.show_plot()

    #ga_player.chromosome.output_action_table(chr_file)



if __name__ == '__main__':
    main()