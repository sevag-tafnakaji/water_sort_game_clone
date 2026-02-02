import random
from Tube import Colour, Tube

class gameStateMachine():

    def __init__(self, seed = 0, verbose = False):
        self.seed = seed  # for repeatable random initial state
        self.verbose = verbose
        self.num_tubes = len(Colour) + 2

        self.states = [Tube(verbose) for _ in range(self.num_tubes)]

    def initialise_states(self):
        if self.verbose:
            self.print_states()

        # create a list of lists with 4 colour each, then flatten it into a mega list
        initial_states = [colour for subcolour in [[colour] * 4 for colour in Colour] for colour in subcolour]
        state_idxs = list(range(self.num_tubes))

        random.shuffle(initial_states)
        random.shuffle(state_idxs)

        for idx, state_idx in enumerate(state_idxs):
            if idx >= len(Colour):
                # self.states[state_idx] = {0: None, 1: None, 2: None, 3: None}
                continue
            state_list_idx = 4 * idx
            current_state = initial_states[state_list_idx:state_list_idx + 4]
            self.states[state_idx] = Tube(values={
                0: current_state[0],
                1: current_state[1],
                2: current_state[2],
                3: current_state[3]
            })

        if self.verbose:
            self.print_states()

    def print_states(self):
        print("-----------------------")
        for state in self.states:
            state.print_tube()
        print("-----------------------")

    def move(self, idx_1: int, idx_2: int):
        """
            Move colours from tube at idx_1 to tube at idx_2

        Args:
            idx_1 (int): _description_
            idx_2 (int): _description_
        """
        if self.verbose:
            print("-----------------------")
            self.states[idx_1].print_tube()
            self.states[idx_2].print_tube()

        # check guard + get neccessary info about how much and what is being moved 
        guard_passed, colour, num_to_move = self.states[idx_1].guard(self.states[idx_2])

        # transition
        if guard_passed:
            if self.verbose:
                print(f"Going to move {colour} into {num_to_move} spaces")
            self.states[idx_1].remove_value(num_to_move, colour)
            self.states[idx_2].add_value(colour, num_to_move)

        if self.verbose:
            self.states[idx_1].print_tube()
            self.states[idx_2].print_tube()

if __name__ == "__main__":
    sm = gameStateMachine(verbose=False)

    sm.initialise_states()
