# Compile with Python3 3.8+
# Required files: main.py, robot.py, map.py
from blackjack import Blackjack
from q_table import Q_Table
from time import sleep

ACTION_COUNT = 4
EPISODES = 20000
GAMES = 200
EPSILON = 0.05
EPSILON_DECREASE_FREQ = 50
EPSILON_DECREASE_RATE = (EPSILON / (EPISODES/EPSILON_DECREASE_FREQ)) * 1.5
LEARNING_RATE = 0.001
DISCOUNT = 0.9
REPORT_FREQUENCY = 100
Q_TABLE_FILE = "q-table.txt"
REPORT_FILE = "reports.txt"
SCORES_FILE = "scores.csv"
ACTION_TABLE_FILE = "action.csv"

BET = 10
DECK_COUNT = 1

score_set = []
highest_score = -999999
epsilon = EPSILON
q_table = Q_Table(ACTION_COUNT)
stored_state = ()
stored_action = ()

for episodes in range(1, EPISODES+1):
    game = Blackjack(BET, DECK_COUNT)
    for games in range(1, GAMES+1):
        state = game.start_hand()
        q_table.set_state(state)
        while (state != None):
            action = q_table.choose_action(epsilon)
            # if (action == game.SPLIT):
            #     stored_state = state
            #     stored_action = action
            #     while (state != None):
            #         state, reward = game.do_action(action)
            #         action = q_table.choose_action(epsilon)
            #         q_table.update_q_table(reward, LEARNING_RATE, DISCOUNT, state)
            #     q_table.set_state(stored_state)
            #     action = stored_action
            #     q_table.update_q_table(reward, LEARNING_RATE, DISCOUNT, state)
            # else:
            state, reward = game.do_action(action)
            q_table.update_q_table(reward[0], LEARNING_RATE, DISCOUNT, state)
            if (len(reward) == 2):
                pass

    score = game.get_score()
    if (score > highest_score):
        highest_score = score
    score_set.append(score)
    if (episodes % EPSILON_DECREASE_FREQ == 0 and epsilon != 0):
        epsilon -= EPSILON_DECREASE_RATE
        if (epsilon < 0):
            epsilon = 0
    if (episodes % REPORT_FREQUENCY == 0):
        avg = sum(score_set) / REPORT_FREQUENCY
        score_set = []
        print(f'Episode: {episodes}  Highest Score: {highest_score}  Last {REPORT_FREQUENCY} Avg Score: {avg}  Epsilon: {epsilon}')    
        q_table.output_q_table(Q_TABLE_FILE)
        with open(SCORES_FILE, "a") as f:
            f.write(f'{episodes},{score},{avg}\n')
        f.close()

q_table.output_action_table(ACTION_TABLE_FILE)

# game = Blackjack(BET, DECK_COUNT)
# game.logs_on(True)
# for games in range(10):
#     print(f'Game: {games}')
#     state = game.start_hand()
#     q_table.starting_state(state)
#     while (state != None):
#         action = q_table.choose_action(epsilon)
#         state, reward = game.do_action(action)





