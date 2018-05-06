import json
import operator
import random


class Action:
    def __init__(self):
        pass

    STAY = 0
    UP = 1
    DOWN = 2


class Bot(object):
    """
    The Bot class that applies the Qlearning logic to Flappy bird game
    After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    After every DUMPING_N iterations, dumps the Q values to the local JSON file
    """

    def __init__(self):
        self.gameCNT = 0  # Game count of current run, incremented after every death
        self.DUMPING_N = 2  # Number of iterations to dump Q values to JSON after
        self.discount = 1.0
        self.reward = {0: 1, 1: -1000}  # Reward function
        self.alpha = 0.7
        self.last_state = None
        self.last_action = 0
        self.q_values = self.load_q_values()
        self.actions = {Action.UP: 'UP', Action.DOWN: 'DOWN', Action.STAY: 'STAY'}
        self.init_state = [0] * (len(self.actions.keys()))
        self.exploration_prob = 5
        self.last_state_eval = False

        # For making exploration as a function of
        # number of games and number of games where score > 200
        self.num_games = 0
        self.num_win_games = 0

    def exploration_val(self):
        return self.exploration_prob / (self.num_win_games + 1)

    @staticmethod
    def load_q_values():
        """
        Load q values from a JSON file
        """
        try:
            q_value_file = open('qvalues.json', 'r')
            q_values = json.load(q_value_file)
            q_value_file.close()
            return q_values
        except (IOError, ValueError) as _:
            return {}

    def act(self, x_diff, y_diff, velocity, score, obstacle=1):
        """
        Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        """
        if x_diff > 100:
            if self.last_state is None:
                # print("first state")
                state = self.map_state(x_diff, y_diff, velocity, obstacle)
                self.last_state = state
                self.last_action = 0
            else:
                self.last_state_eval = False
                return 0
        else:
            state = self.map_state(x_diff, y_diff, velocity, obstacle)
            self.last_state = state
            self.last_state_eval = True
            if state not in self.q_values:
                self.q_values[state] = self.init_state
                self.last_action = 0
            else:
                best_action = self.get_best_action(state)
                self.last_action = best_action
        return self.last_action

    def get_last_state(self):
        return self.last_state

    def update_q_values(self, game_param, is_dead=False, user_event=None):
        """
        Update qvalues via iterating over experiences
        """
        state = self.last_state
        if user_event is None:
            act = self.last_action
        else:
            act = user_event
            # print("intervention {}".format(act))
        x_diff, y_diff, velocity, type_obstacle = game_param
        res_state = self.map_state(x_diff, y_diff, velocity, type_obstacle)
        if self.last_state_eval:
            # if state not in self.q_values:
            #     self.q_values[state] = self.init_state
            if res_state not in self.q_values:
                self.q_values[res_state] = self.init_state
            self.q_values[state][act] = (1 - self.alpha) * (self.q_values[state][act]) + self.alpha * (
                    self.reward[int(is_dead)] + self.discount * max(self.q_values[res_state]))
        if is_dead:
            self.gameCNT += 1  # increase game count
            self.dump_q_values()  # Dump q values (if game count % DUMPING_N == 0)

    @staticmethod
    def map_state(x_diff, y_diff, velocity, obstacle=1):
        return "{}_{}_{}_{}".format(int(x_diff), int(y_diff), velocity, obstacle)

    def dump_q_values(self):
        """
        Dump the qvalues to the JSON file
        """
        if self.gameCNT % self.DUMPING_N == 0:
            fil = open('qvalues.json', 'w')
            json.dump(self.q_values, fil)
            fil.close()
            print('Q-values updated on local file.')

    def get_best_action(self, state):
        # action_q_value = map(lambda action: self.q_values[state][action], self.actions.keys())
        # max_index, _ = max(enumerate(action_q_value), key=operator.itemgetter(1))
        # return max_index
        exp_val = self.exploration_val()
        epsilon = random.randint(1, 100) < exp_val
        if epsilon:
            # print(exp_val)
            # print("Trying exploration")
            return random.randint(0, 2)
        else:
            action_q_value = map(lambda action: self.q_values[state][action], self.actions.keys())
            max_index, _ = max(enumerate(action_q_value), key=operator.itemgetter(1))
            return max_index
