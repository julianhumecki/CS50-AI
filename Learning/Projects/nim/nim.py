import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        #list of piles
        self.piles = initial.copy()
        #player turn
        self.player = 0
        #winner
        self.winner = None

    @classmethod
    # returns a set of all actions
    # you can take
    # argument is the class
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        #keep track of index and index value
        for i, pile in enumerate(piles):
            for j in range(1, piles[i] + 1):
                actions.add((i, j))
        return actions

    @classmethod
    #determine the opponent
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    #performs action on the current state
    #and switches the player's turn
    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        #this keeps track of all Q(s,a) values learned by our AI
        #maps (state, action) to a numerical value
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon


    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        #gets the current q value
        old = self.get_q_value(old_state, action)
        #gets the best future reward with this new state
        best_future = self.best_future_reward(new_state)
        #update the q value
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        #if this state, action value doesn't exist
        #return 0
        if not (tuple(state), action) in self.q:
            return 0
        #otherwise return the mapping value
        return self.q[tuple(state), action]
        

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        #implement the q learning algorithm 
        self.q[tuple(state), action] = old_q + self.alpha * (reward + future_rewards - old_q)
        return 

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        actions = self.get_all_actions(state)
        #base case of there being no available actions to make
        if len(actions) == 0:
            return 0
        #can take one of N actions
        max_value = -1
        best_action = None
        for action in actions:
            #get the value of the action
            value = -1
            #if action not done before
            #value of 0, unknown if good or bad, learn from it
            if not (tuple(state), action) in self.q:
                value = 0
            else: 
                value = self.q[tuple(state), action]

            if value > max_value:
                max_value = value
                best_action = action
        
        return max_value
        

    def get_all_actions(self,state):
        actions = set()
        for i, block_count in enumerate(state):
            #in range doesn't include the upper bound
            #[lower, upper)
            for j in range(1, state[i] + 1):
                actions.add((i, j))
        return actions

    #select an action to take using
    #epsilon - greedy
    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        #base case of nothing being known
        actions = self.get_all_actions(state)
        #print(len(actions))
        #print(f"Actions: {actions}")
        #print(f"epsilon: {epsilon}")
        #print(f"epsilon value: {self.epsilon}")
        randomness = []
        #make random move probability epsilon
        randomness += [0]*math.ceil(100*self.epsilon)
        #make best move probability 1 - e
        randomness += [1]*math.ceil(100*(1 - self.epsilon))
        choice = random.choice(randomness)
        #print(randomness)
        if len(self.q) == 0 or len(actions) == 0:
            return random.choice(list(actions))

        #make best move if not epsilon
        if not epsilon:
            return self.best_action(state, actions)
        #make best move with probability (1 - epsilon)
        else:
            #best move choice
            if choice == 1:
                #print("Best")
                tup = self.best_action(state, actions)
                #print(f"Tuple: {tup}")
                return tup
            #random action
            #print("worst")
            tup = random.choice(list(actions))
            #print(f"Tuple: {tup}")
            return tup


    def best_action(self, state, actions):
        
        
        #base case of there being no available actions to make
        #print("In best_action:")
        if len(actions) == 0:
            #print("Issue")
            return None
        #can take one of N actions
        max_value = -1000000
        best_action = None
        for action in actions:
            #get the value of the action
            value = -1
            #if action not done before
            #value of 0, unknown if good or bad, learn from it
            if not (tuple(state), action) in self.q:
                #print("Not in")
                value = 0
            else: 
                #print("In")
                #print(f"Self q value: {self.q[tuple(state), action]}")
                value = self.q[tuple(state), action]

            #print(f"Value: {value}")
            #print(f"Max value: {max_value}")
            if value > max_value:
                #print("Updated...")
                max_value = value
                best_action = action
        
        return best_action
        


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
