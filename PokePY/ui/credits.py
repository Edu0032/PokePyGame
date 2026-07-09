import sys

import pygame

from PokePY.config import SCREEN_CONFIG
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook

class CreditsScreen:
    def __init__(self, fonts: FontBook):
        self.fonts = fonts
        self.lines = [
            "PokePy - Fim da Jornada",
            "",
            "Créditos Especiais",
            "",
            "Sprites: João Lucas",
            "Sprite do avatar: Prima do Eduardo",
            "Sprite do mapa: Eduardo",
            "Sistema de mochila: Jéssica",
            "Tela inicial: Luiz",
            "Sistema de batalha: Maycon",
            "",
            "Equipe de Apoio",
            "Animações: Maycon",
            "Roteiro: Jéssica e Eduardo",
            "Design de UI: João Lucas e Maycon",
            "Balanceamento: Luiz",
            "Cenários: Eduardo",
            "Testes: Maycon",
            "Programação auxiliar: Luiz",
            "Ilustrações: Eduardo",
            "Consultoria Pokémon: Maycon",
            "Documentação: Maycon e Luiz",
            "Gerenciamento: Jéssica",
            "Agradecimentos especiais: comunidade Python e Pygame",
            "",
            "",
            "Obrigado por jogar!",
        ]

    def show(self, screen: pygame.Surface):
        clock = pygame.time.Clock()
        fade_surface = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height))
        fade_surface.fill(colors.BLACK)
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(30)
        y_offset = SCREEN_CONFIG.height + 50
        while True:
            screen.fill(colors.BLACK)
            for index, line in enumerate(self.lines):
                font = self.fonts.credits_big if index == 0 else self.fonts.credits
                text_color = colors.WHITE if index == 0 else (230, 230, 230)
                surface = font.render(line, True, text_color)
                rect = surface.get_rect(center=(SCREEN_CONFIG.width // 2, y_offset + index * 40))
                screen.blit(surface, rect)
            pygame.display.flip()
            clock.tick(SCREEN_CONFIG.fps)
            y_offset -= 1.2
            if y_offset + len(self.lines) * 40 < -50:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    return
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(20)
        pygame.quit()
        sys.exit()
