import pygame

class Button:
    def __init__(self, inactive, active, position):
        self.img_inactive = pygame.image.load(inactive)
        self.img_active = pygame.image.load(active)
        self.active = False
        self.position = position
    
    def draw(self, surface):
        if self.active:
            surface.blit(self.img_active, self.position)
        else:
            surface.blit(self.img_inactive, self.position)
        
    def do(self, surface):
        pass
        