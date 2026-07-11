import pygame


class FontBook:
    def __init__(self):
        if not pygame.font.get_init():
            pygame.font.init()
        self.small = pygame.font.SysFont(None, 18)
        self.medium = pygame.font.SysFont("arial", 18, bold=True)
        self.normal = pygame.font.SysFont(None, 24)
        self.large = pygame.font.SysFont(None, 30)
        self.xl = pygame.font.SysFont(None, 40)
        self.credits = pygame.font.SysFont("Arial", 26, bold=True)
        self.credits_big = pygame.font.SysFont("Arial", 40, bold=True)
