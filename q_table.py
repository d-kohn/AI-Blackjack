
from random import random, randrange

class Q_Table():
    ACTION_COUNT = 3
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    SPLIT = 3

    def __init__(s, action_count=0):
        s.action_count = action_count
        s.q_table = {}
        s.state = ()
        s.prev_state = ()
        s.action = 0

        # for player_hand_state in range(4, 31):
        #     for dealer_hand_state in range(2, 12):
        #         for round in range (1, 3):
        #             s.q_table[tuple([player_hand_state, dealer_hand_state, round])] = [0,0,0,0]

        for hand_state in range(4, 40):
            for dealer_hand_state in range(2, 12):
                for round in range (1, 3):
                        s.q_table[tuple([hand_state, dealer_hand_state, round])] = [0,0,0,0]

    def read_in(self, filename):
        file = open(filename, 'r')
        empty = False
        #readline first is key, second is val, repeat
        while not empty:
            key_line = file.readline()
            if not key_line:
                empty = True
                break
            value_line = file.readline()

            key_list = []
            for item in key_line:
                key_list.append(item)
            value_list = []
            for value in value_line:
                value_list.append(value)

            self.q_table[tuple(key_list)] = value_list




    def update_q_table(s, reward, eta, discount, new_state):
        s.prev_state = s.state
        prev_state_actions = s.q_table[s.prev_state]
        s.state = new_state
        if (new_state != None):
            current_state_actions = s.q_table[new_state]
            current_state_max_reward = 0

            for action in range(s.action_count):
                if (current_state_actions[action] > current_state_max_reward):
                    current_state_max_reward = current_state_actions[action]
        
            (s.q_table[s.prev_state])[s.action] = prev_state_actions[s.action] + eta * (reward + discount * current_state_max_reward - prev_state_actions[s.action])
        else:
            current_state_max_reward = 0
            (s.q_table[s.prev_state])[s.action] = prev_state_actions[s.action] + eta * (reward + discount * current_state_max_reward - prev_state_actions[s.action])
            

    def choose_action(s, epsilon=0):
        current_state = s.q_table[s.state]
        if (1 - epsilon < random()):
            return randrange(s.action_count)
        # Do greedy action
        else:
            best_actions = [0]
            for action in range(1, s.action_count):
                if (int(current_state[action]*100) > int(current_state[best_actions[0]]*100)):
#                if (current_state[action]) > current_state[best_actions[0]]:
                    best_actions = [action]
                elif (int(current_state[action]*100) == int(current_state[best_actions[0]]*100)):
#                elif (current_state[action]) == current_state[best_actions[0]]:
                        best_actions.append(action)   
        
            if (len(best_actions) == 1):
                s.action = best_actions[0]
            else:
                index = randrange(len(best_actions))
                s.action = best_actions[index]
        return s.action

    def starting_state(s, new_state):
        s.state = new_state

    def output_q_table(s, file):
        with open(file, "w") as f:
            for state in s.q_table:
                if (sum(s.q_table[state]) != 0):
                    f.write(f'{state}\n')
                    f.write(f'{s.q_table[state]}\n')
        f.close()

    def output_action_table(s, file):
        with open(file, "w") as f:
            for r in range(1,3):
                f.write(f'Round {r}\n')
                for hand_state in range(5, 41):
                    for dealer in range(2, 12):
                        key = tuple([hand_state,dealer,r])
                        if (sum(s.q_table[key]) != 0):
                            best = 0                           
                            for i in range(1, s.action_count):
                                if ((s.q_table[key])[i] > (s.q_table[key])[best]):
                                    best = i
                            f.write(f'{s.action_string[best]},')
                    f.write('\n')
        f.close()

    action_string = {
        0 : 'HIT',
        1 : 'STAND',
        2 : 'DOUBLE DOWN',
        3 : 'SPLIT'
    }