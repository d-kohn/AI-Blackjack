# Compile with Python3 3.8+
# Required files: main.py, robot.py, map.py
from blackjack import Blackjack
from q_table import Q_Table
from time import sleep

ACTION_COUNT = 4
EPISODES = 10000
GAMES = 200
EPSILON = 0.05
EPSILON_DECREASE_FREQ = 50
EPSILON_DECREASE_RATE = (EPSILON / (EPISODES/EPSILON_DECREASE_FREQ)) * 1.5
LEARNING_RATE = 0.001
DISCOUNT = 0.9
REPORT_FREQUENCY = 200
Q_TABLE_FILE = "q-table.txt"
REPORT_FILE = "reports.txt"
SCORES_FILE = "scores.csv"
ACTION_TABLE_FILE = "action.csv"

BET = 10
DECK_COUNT = 1


q_table = Q_Table(ACTION_COUNT)

def train(q_table : Q_Table):
    score_set = []
    highest_score = -999999
    epsilon = EPSILON
    stored_state = ()
    stored_action = 0

    for episodes in range(1, EPISODES+1):
        game = Blackjack(BET, DECK_COUNT)
        score = 0
        for _ in range(1, GAMES+1):    
            state = game.start_hand()            
            q_table.set_state(state)
            while (state != None):
                action = q_table.choose_action(state, epsilon)
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
                q_table.update_q_table(sum(reward), LEARNING_RATE, DISCOUNT, state)
                if (sum(reward) > 0):
                   score += sum(reward)
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
            print(f'Episode: {episodes}  Highest Score: {highest_score}  Last {REPORT_FREQUENCY} Avg Score: {round(avg, 1)}  / {GAMES*BET}  Epsilon: {round(epsilon, 6)}')    
            q_table.output_q_table(Q_TABLE_FILE)
            with open(SCORES_FILE, "a") as f:
                f.write(f'{episodes},{score},{avg}\n')
            f.close()
    q_table.output_action_table(ACTION_TABLE_FILE)

train(q_table)
#game.logs_on(True)
#q_table.read_in('q-table.txt')
score = 0
overall_score = 0
GAME_COUNT = 2000

for episodes in range (1, GAME_COUNT+1):
    game = Blackjack(BET, DECK_COUNT)
    score = 0
    for _ in range(GAMES):    
        state = game.start_hand()            
        while (state != None):
            action = q_table.choose_action(state, 0)
            state, reward = game.do_action(action)

            if (sum(reward) > 0):
                score += sum(reward)
    overall_score += score
    if (episodes % 100 == 0):
        print(f'Episodes: {episodes}  Player Score Average: {round(overall_score/episodes, 2)} / {GAMES*BET}')    

print(f'Hands played: {GAME_COUNT*GAMES}  Player Score : {round(overall_score/episodes, 2)} / {GAMES*BET}')


