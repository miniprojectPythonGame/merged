from .ImageField import ImageField

from src.globals.const_values import *


class ItemBox:
    def __init__(self, x, y, width, height, screen, color=pygame.Color('#555555'),
                 active_color=pygame.Color('#c73434'), fill=None, path=None, border=2,
                 offset=0, border_radius=0, isActive=False, id=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fill = fill
        self.screen = screen
        self.path = path
        self.border = border
        self.border_radius = border_radius
        self.offset = offset
        self.isActive = isActive
        self.active_color = active_color
        self.id = id
        self.image = ImageField(x + offset, y + offset,
                                width - 2 * offset, height - 2 * offset,
                                path, screen)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        if self.fill is not None:
            pygame.draw.rect(self.screen, self.fill, self.rect, 0, self.border_radius)

        if self.isActive:
            pygame.draw.rect(self.screen, self.active_color, self.rect, self.border, self.border_radius)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect, self.border, self.border_radius)

        self.image.draw()

    def activate(self):
        self.isActive = True

    def deactivate(self):
        self.isActive = False