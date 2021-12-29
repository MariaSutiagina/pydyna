import sys
import pygame

class Game:
    def __init__(self, frame_rate, statemodel):
        self.frame_rate = frame_rate
        self.statemodel = statemodel

    def get_state(self):
        return None

    def update(self):
        for o in self.get_state().objects:
            o.update_state()

    def draw(self):
        for o in self.get_state().objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.get_state().keydown_handlers[event.key]:
                    handler(event.key, pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                for handler in self.get_state().keyup_handlers[event.key]:
                    handler(event.key, pygame.key.get_pressed())
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.get_state().mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while not self.statemodel.is_game_state_QuitGame():
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
