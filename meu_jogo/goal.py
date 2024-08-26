import pygame
import os

class Goal:
    def __init__(self, pos, size=100):
        self.pos = pos
        self.size = size
        caminho = os.path.join(os.path.dirname(__file__), 'images', 'casa_do_vizinho.png')
        self.image = pygame.image.load(caminho)
        self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self, screen):
        """Desenha o objetivo na tela."""
        screen.blit(self.image, self.pos)  # Desenha a imagem na tela na posição especificada

    def check_collision(self, projectile):
        """Verifica se o projétil colidiu com o objetivo."""
        proj_x, proj_y = projectile.pos
        goal_x, goal_y = self.pos
        if (goal_x <= proj_x <= goal_x + self.size) and (goal_y <= proj_y <= goal_y + self.size):
            return True
        return False
