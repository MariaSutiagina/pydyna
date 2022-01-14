from pygame import Surface
from pygame.rect import Rect


class CustomObject:
    def __init__(self, x, y, w, h):
        self.bounds = Rect(x, y, w, h)

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface:Surface):
        pass

    def get_sort_key(self):
        return 0
        
    def update_state(self):
        pass
