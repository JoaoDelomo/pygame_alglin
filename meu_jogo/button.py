import pygame

class CloseButton:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.button_size = 30
        self.button_x = width - self.button_size - 10
        self.button_y = 10
        self.color = (255, 0, 0)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.button_x, self.button_y, self.button_size, self.button_size))
        font = pygame.font.SysFont(None, 24)
        text = font.render('X', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.button_x + self.button_size // 2, self.button_y + self.button_size // 2))
        self.screen.blit(text, text_rect)

    def is_clicked(self, pos):
        mouse_x, mouse_y = pos
        if self.button_x <= mouse_x <= self.button_x + self.button_size and self.button_y <= mouse_y <= self.button_y + self.button_size:
            return True
        return False
