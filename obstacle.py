import pygame

class Obstacle:
    def __init__(self, pos, size):
        self.pos = list(pos)
        self.size = list(size)
        self.color = (139, 69, 19)  # Cor inicial do obstáculo (marrom)
        self.health = 3  # Cada obstáculo tem 3 pontos de vida

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, *self.size))

    def hit(self):
        # Reduzir a vida do obstáculo ao ser atingido
        self.health -= 1
        if self.health <= 0:
            return True  # Indica que o obstáculo deve ser removido
        else:
            # Escurecer a cor do obstáculo para indicar dano
            self.color = tuple(max(0, c - 50) for c in self.color)
            return False
