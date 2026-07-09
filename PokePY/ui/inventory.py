import pygame

from PokePY.config import SCREEN_CONFIG, UI_CONFIG
from PokePY.domain.models import Player
from PokePY.infrastructure.assets import AssetLoader
from PokePY.ui import colors
from PokePY.ui.fonts import FontBook
from PokePY.ui.widgets import draw_round_button, draw_text, is_button_clicked

class InventoryView:
    def __init__(self, fonts: FontBook, assets: AssetLoader):
        self.fonts = fonts
        self.assets = assets

    def draw(self, screen: pygame.Surface, player: Player) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        screen.fill(colors.PANEL_PAGE_BACKGROUND)
        box_x = (SCREEN_CONFIG.width - UI_CONFIG.inventory_width) // 2
        box_y = (SCREEN_CONFIG.height - UI_CONFIG.inventory_height) // 2
        box_rect = pygame.Rect(box_x, box_y, UI_CONFIG.inventory_width, UI_CONFIG.inventory_height)
        pygame.draw.rect(screen, colors.PANEL_BACKGROUND, box_rect, border_radius=25)
        pygame.draw.rect(screen, colors.PANEL_BORDER, box_rect, 3, border_radius=25)
        icon = self.assets.load_backpack_icon(40)
        title_surface = self.fonts.xl.render("MOCHILA", True, (40, 40, 70))
        title_rect = title_surface.get_rect(center=(SCREEN_CONFIG.width // 2 + 20, box_y + 50))
        if icon:
            icon_rect = icon.get_rect()
            total_width = icon_rect.width + 10 + title_rect.width
            start_x = (SCREEN_CONFIG.width - total_width) // 2
            icon_rect.topleft = (start_x, box_y + 30)
            title_rect.topleft = (start_x + icon_rect.width + 10, box_y + 35)
            screen.blit(icon, icon_rect)
        screen.blit(title_surface, title_rect)
        repel_rect = draw_round_button(screen, self.fonts, box_y + 120, colors.BAG_BLUE, f"Usar Repelente ({player.items.get('Repelente', 0)})", SCREEN_CONFIG.width // 2)
        potion_rect = draw_round_button(screen, self.fonts, box_y + 200, colors.BAG_GREEN, f"Usar Poção ({player.items.get('Poção', 0)})", SCREEN_CONFIG.width // 2)
        close_rect = draw_round_button(screen, self.fonts, box_y + 300, colors.BAG_RED, "Fechar Mochila", SCREEN_CONFIG.width // 2)
        return repel_rect, potion_rect, close_rect

    def select_pokemon_for_heal(self, screen: pygame.Surface, player: Player) -> str:
        if player.items.get("Poção", 0) <= 0:
            return "no_potion"
        while True:
            screen.fill((235, 238, 245))
            box_width = 500
            box_height = 450
            box_x = (SCREEN_CONFIG.width - box_width) // 2
            box_y = (SCREEN_CONFIG.height - box_height) // 2
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, colors.WHITE, box_rect, border_radius=25)
            pygame.draw.rect(screen, colors.PANEL_BORDER, box_rect, 3, border_radius=25)
            draw_text(screen, self.fonts, "Escolha um Pokémon para curar:", SCREEN_CONFIG.width // 2, box_y + 40, color=(50, 50, 80), font=self.fonts.xl, center=True)
            buttons = []
            for index, pokemon in enumerate(player.team):
                rect = draw_round_button(screen, self.fonts, box_y + 100 + index * 60, (100, 150, 255), f"{pokemon.name} (HP: {pokemon.hp}/{pokemon.max_hp})", SCREEN_CONFIG.width // 2, width=350, height=45)
                buttons.append((rect, pokemon))
            back_rect = draw_round_button(screen, self.fonts, box_y + 100 + len(player.team) * 60 + 50, colors.BAG_RED, "Voltar", SCREEN_CONFIG.width // 2, width=350, height=45)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if is_button_clicked(mouse_pos, back_rect):
                        return "canceled"
                    for rect, pokemon in buttons:
                        if is_button_clicked(mouse_pos, rect):
                            pokemon.heal(50)
                            player.items["Poção"] -= 1
                            return "healed"
