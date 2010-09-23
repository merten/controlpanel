"""
This Primitiv button is only displayed no further function.
"""

import pygame

class Button:
    def __init__(self, inactive, active, position):
        """
        Args:
            inactiv: Path to inactiv button picture.
            active: Path to activ buttin picture.
            position: Position on the target surface.
        """
        self.img_inactive = pygame.image.load(inactive)
        self.img_active = pygame.image.load(active)
        self.active = False
        self.position = position
    
    def draw(self, surface):
        if self.active:
            surface.blit(self.img_active, self.position)
        else:
            surface.blit(self.img_inactive, self.position)