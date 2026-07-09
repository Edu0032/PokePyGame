import pygame

from PokePY.ui import colors
from PokePY.ui.fonts import FontBook

def draw_text(screen: pygame.Surface, fonts: FontBook, text, x: int, y: int, color=colors.BLACK, font=None, center=False, center_y=False, align_right=False):
    selected_font = font or fonts.normal
    surface = selected_font.render(str(text), True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    elif align_right:
        rect.right = x
        rect.centery = y
    elif center_y:
        rect.midleft = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect

def draw_rounded_box(screen: pygame.Surface, rect, color, radius=10, shadow_color=None, shadow_offset=(3, 3)):
    rect = rect if isinstance(rect, pygame.Rect) else pygame.Rect(rect)
    if shadow_color is not None:
        shadow_rect = pygame.Rect(rect.x + shadow_offset[0], rect.y + shadow_offset[1], rect.width, rect.height)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=radius)
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    return rect

def draw_styled_button(screen: pygame.Surface, fonts: FontBook, text: str, rect, text_color=colors.BLACK, bg_color=colors.BATTLE_BUTTON_NORMAL, hover_color=colors.BATTLE_BUTTON_HOVER, selected=False, mouse_pos=None, font=None):
    rect = rect if isinstance(rect, pygame.Rect) else pygame.Rect(rect)
    current_bg = bg_color
    shadow_offset = (2, 2)
    if selected:
        current_bg = colors.BATTLE_BUTTON_SELECTED
        shadow_offset = (0, 0)
    elif mouse_pos and rect.collidepoint(mouse_pos):
        current_bg = hover_color
        shadow_offset = (1, 1)
    shadow_rect = rect.move(*shadow_offset)
    pygame.draw.rect(screen, colors.SHADOW_COLOR_DARK, shadow_rect, border_radius=8)
    pygame.draw.rect(screen, current_bg, rect, border_radius=8)
    pygame.draw.rect(screen, colors.BATTLE_MENU_BORDER, rect, 1, border_radius=8)
    draw_text(screen, fonts, text, rect.centerx, rect.centery, color=text_color, font=font or fonts.large, center=True)
    return rect

def draw_round_button(screen: pygame.Surface, fonts: FontBook, y: int, color, text: str, center_x: int, width: int = 350, height: int = 50):
    rect = pygame.Rect(center_x - width // 2, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, colors.BAG_BUTTON_BORDER, rect, 2, border_radius=15)
    draw_text(screen, fonts, text, rect.centerx, rect.centery, color=colors.BAG_BUTTON_TEXT, font=fonts.large, center=True)
    return rect

def is_button_clicked(mouse_pos, rect) -> bool:
    if isinstance(rect, pygame.Rect):
        return rect.collidepoint(mouse_pos)
    if isinstance(rect, (tuple, list)) and len(rect) == 4:
        x, y, w, h = rect
        return x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
    return False

def draw_modal_message(screen: pygame.Surface, fonts: FontBook, message: str, bg_color=colors.BATTLE_MENU_BG, border_color=colors.BATTLE_MENU_BORDER, text_color=colors.DARK_BLUE):
    from PokePY.config import SCREEN_CONFIG, UI_CONFIG
    overlay = pygame.Surface((SCREEN_CONFIG.width, SCREEN_CONFIG.height), pygame.SRCALPHA)
    overlay.fill(colors.OVERLAY_DARK)
    screen.blit(overlay, (0, 0))
    rect = pygame.Rect((SCREEN_CONFIG.width - UI_CONFIG.modal_width) // 2, (SCREEN_CONFIG.height - UI_CONFIG.modal_height) // 2, UI_CONFIG.modal_width, UI_CONFIG.modal_height)
    draw_rounded_box(screen, rect, bg_color, radius=15, shadow_color=colors.SHADOW_COLOR_DARK, shadow_offset=(5, 5))
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=15)
    draw_text(screen, fonts, message, rect.centerx, rect.centery, color=text_color, font=fonts.xl, center=True)
    return rect
