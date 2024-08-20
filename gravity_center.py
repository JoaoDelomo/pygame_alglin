import pygame
import math

class GravityCenter:
    def __init__(self, pos, strength, influence_radius):
        self.pos = pos  # Posição do centro gravitacional
        self.strength = strength  # Força gravitacional
        self.influence_radius = influence_radius  # Raio de influência do centro gravitacional

    def draw(self, screen):
        # Desenhar o centro gravitacional
        pygame.draw.circle(screen, (255, 0, 0), self.pos, 15)

        # Desenhar a área de influência como um círculo transparente (opcional)
        influence_color = (255, 0, 0, 50)
        influence_surface = pygame.Surface((self.influence_radius * 2, self.influence_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(influence_surface, influence_color, (self.influence_radius, self.influence_radius), self.influence_radius)
        screen.blit(influence_surface, (self.pos[0] - self.influence_radius, self.pos[1] - self.influence_radius))

    def apply_gravity(self, projectile):
        # Calcular a distância entre o projétil e o centro gravitacional
        dx = self.pos[0] - projectile.pos[0]
        dy = self.pos[1] - projectile.pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0 or distance > self.influence_radius:
            return  # Evitar divisão por zero e agir apenas se dentro do raio de influência

        # Aumentar a força gravitacional
        force = (self.strength * 3) / (distance**2)  # Aumentar a força em 3x

        # Calcular a direção da força
        force_x = force * (dx / distance)
        force_y = force * (dy / distance)

        # Aplicar a força ao projétil
        projectile.velocity[0] += force_x
        projectile.velocity[1] += force_y
