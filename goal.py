import pygame

class Goal:
    def __init__(self, pos, size=20):
        self.pos = pos  # Posição do objetivo (canto superior esquerdo)
        self.size = size  # Tamanho do quadrado do objetivo

    def draw(self, screen):
        """Desenha o objetivo na tela."""
        pygame.draw.rect(screen, (0, 255, 0), (*self.pos, self.size, self.size))  # Verde

    def check_collision(self, projectile):
        """Verifica se o projétil colidiu com o objetivo."""
        proj_x, proj_y = projectile.pos
        goal_x, goal_y = self.pos
        if (goal_x <= proj_x <= goal_x + self.size) and (goal_y <= proj_y <= goal_y + self.size):
            return True
        return False
