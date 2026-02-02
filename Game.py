from typing import Tuple

import pygame
from pygame.locals import *
from StateMachine import gameStateMachine
from Tube import Tube, Colour

class Program:
    def __init__(self, state_machine: gameStateMachine):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 600
        self.sm = state_machine

        self.x_padding = 100  # pixel value of padding on each side of screen
        self.y_padding = 30  # pixel value of padding on each side of screen


        self.box_width, self.box_height = 60, 40

    def get_tube_xy(self, tube_idx: int) -> Tuple[int, int]:
        self.usable_width = self.width - 2 * self.x_padding
        self.usable_height = self.height - 2 * self.y_padding

        # TODO: Dynamic sizing of rows and columns based on num tubes (based on size of Colours enum)
        n_per_row = 4

        row_idx = tube_idx // n_per_row
        col_idx = tube_idx % n_per_row

        x_padding_tube = 30
        y_padding_tube = 50
    
        x = self.x_padding + (self.usable_width / n_per_row + x_padding_tube) * col_idx
        y = self.y_padding + (self.usable_height / n_per_row + y_padding_tube) * row_idx

        return x, y

    def render_rect(self, colour: Tuple[int, int, int], x: int, y: int):
        pygame.draw.rect(self._display_surf, colour, (x, y, self.box_width, self.box_height))

    def render_nth_block(self, colour, x, y, n):
        """Render Nth block in a tube, n != index, n in [1, 2, 3, 4]

        Args:
            colour (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            n (_type_): _description_
        """
        new_y = y+self.box_height * (n - 1)
        self.render_rect(colour, x, new_y)

    def render_tube(self, x: int, y: int):
        padding = 5
        height = self.box_height * 4 + 2 * padding
        width = self.box_width + 2 * padding

        pygame.draw.rect(self._display_surf, (255, 255, 255), (x - padding, y - padding, width, height), 1)

    def render_state(self, x, y, state: Tube):
        
        for idx, colour in enumerate(state.values.values()):
            if colour:
                self.render_nth_block(colour.name, x, y, idx + 1)

        self.render_tube(x, y)

    def render_states(self):
        for idx, state in enumerate(self.sm.states):
            x, y = self.get_tube_xy(idx)
            self.render_state(x, y, state)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        # gray background
        self._display_surf.fill((120, 120, 120))

        self.sm.initialise_states()

        self._running = True

    def on_event(self, event: int):
        if event.type == pygame.QUIT:
            self._running = False
        
    def on_loop(self):
        pass

    def on_render(self):
        self.render_states()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
        
        self.on_cleanup()


if __name__ == "__main__":
    a = Program(gameStateMachine())
    a.on_execute()    
