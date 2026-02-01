from enum import Enum
from typing import Dict, Optional, Tuple
from termcolor import colored


class Colour(Enum):
    Red = 1
    Blue = 2
    Green = 3
    Yellow = 4

enum_to_colour = {
    Colour.Red: 'red',
    Colour.Blue: 'blue',
    Colour.Green: 'yellow'
}


class Tube:
    
    # Tube will always hold 4, 0 = top, 3 = bottom
    def __init__(self, verbose = False, values: Optional[Dict[int, Colour]] = None):
        self.verbose = verbose
        self.values = values if values else {0: None, 1: None, 2: None, 3: None}
    
    def get_colours_to_be_moved(self) -> Tuple[Colour, int]:
        # Get how many will move from this tube
        num_to_move = 0

        top_colour: Colour = None

        for this_colour in self.values.values():
            # initialise the colour we want to move
            if top_colour == None and this_colour == None:
                continue
            elif top_colour == None and this_colour != None:
                top_colour = this_colour

            # for each colour after the first that is the same, increment
            if this_colour == top_colour:
                num_to_move += 1
            else:
                # stop as soon as another colour is found
                break 

        return (top_colour, num_to_move)


    def guard(self, other_tube: 'Tube') -> Tuple[bool, Colour, int]:
        
        top_colour, num_to_move = self.get_colours_to_be_moved()

        if self.verbose:
            print(f"Moving colour {top_colour}, can take up {num_to_move} spaces")

        tube_has_space = False
        top_colour_matches = False
        num_empty_spaces = 0

        for other_colour in other_tube.values.values():
            if other_colour != None:
                break

            num_empty_spaces += 1

        tube_has_space = num_empty_spaces > 0
        other_tube_empty = (num_empty_spaces == 4)

        if num_empty_spaces < 4:
            top_colour_matches = other_tube.values[num_empty_spaces] == top_colour            

        tube_valid_colour = other_tube_empty or top_colour_matches

        if self.verbose:
            print(f"Number of empty spaces found in the other tube: {num_empty_spaces}")

        num_empty_spaces = min(num_empty_spaces, num_to_move)
    
        if self.verbose:
            print(f"Other tube has space: {tube_has_space}\nTop colour in other tube matches: {tube_valid_colour}")
        
        guard_pass = (tube_has_space and tube_valid_colour)

        if self.verbose:
            print(f"Guard passed: {guard_pass}")

        return (guard_pass, top_colour, num_empty_spaces)
    
    def add_value(self, colour, num_to_add):
        """
            Should have passed the guard!!!

        Args:
            colour (_type_): _description_
            num_to_add (_type_): _description_
        """
        if self.verbose:
            print("Adding")

        idx_to_start = 0

        first_existing_colour_idx = [idx for idx in range(4) if(self.values[idx] is None)]

        if len(first_existing_colour_idx) > 0:
            idx_to_start = len(first_existing_colour_idx) - 1

        if self.verbose:
            print(colour, first_existing_colour_idx, idx_to_start)

        for i in range(idx_to_start, idx_to_start - num_to_add, -1):
            if self.verbose:
                print(i)
            self.values[i] = colour

    def remove_value(self, num_to_remove, colour):
        """
            Should have passed the guard!!!

        Args:
            colour (_type_): _description_
            num_to_remove (_type_): _description_
        """
        if self.verbose:
            print("Removal")
        idx_to_start = 0

        first_existing_colour_idxs = []#[idx for idx in range(4) if(self.values[idx] in [None, colour])]

        for idx in range(4):
            if self.values[idx] in [None]:
                first_existing_colour_idxs.append(idx)
            else:
                break

        if self.verbose:
            print(first_existing_colour_idxs)

        if len(first_existing_colour_idxs) > 0:
            idx_to_start = len(first_existing_colour_idxs)

        if self.verbose:
            print(idx_to_start, num_to_remove)

        for i in range(idx_to_start, idx_to_start + num_to_remove):
            if self.verbose:
                print(i)
            self.values[i] = None

    def print_tube(self):
        msg = ""

        for colour in self.values.values():
            if colour:
                msg += f": {colored(colour.name.upper(), colour.name.lower())} :"
            else:
                msg += f":       :"

        print(msg)
