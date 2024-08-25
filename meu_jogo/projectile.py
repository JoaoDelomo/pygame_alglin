import pygame
import math

class Projectile:
    def __init__(self, pos, screen_width, screen_height, size=50):
        self.initial_pos = list(pos)
        self.pos = list(pos)
        self.angle = 0
        self.power = 0
        self.velocity = [0, 0]
        self.gravity = 2
        self.launched = False
        self.slowdown_factor = 0.05  # Fator para desacelerar o movimento
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size  # Novo tamanho do projétil

        # Carregar o sprite do projétil
        self.sprite = pygame.image.load("images/jaca.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))  # Ajuste o tamanho conforme necessário

    def calculate_velocity(self):
        self.velocity = [
            self.power * math.cos(math.radians(self.angle)),
            -self.power * math.sin(math.radians(self.angle))
        ]

    def update(self):
        if self.launched:
            # Atualizar a posição da bola
            self.velocity[1] += self.gravity * self.slowdown_factor
            self.pos[0] += self.velocity[0] * self.slowdown_factor
            self.pos[1] += self.velocity[1] * self.slowdown_factor

            # Verificar se o projétil tocou a borda da tela
            if (self.pos[0] < 0 or self.pos[0] > self.screen_width or
                self.pos[1] < 0 or self.pos[1] > self.screen_height):
                self.reset()

    def draw(self, screen):
        # Desenhar o sprite na posição do projétil
        sprite_rect = self.sprite.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(self.sprite, sprite_rect)

    def reset(self):
        self.pos = list(self.initial_pos)
        self.launched = False
        self.velocity = [0, 0]

    def launch(self):
        self.launched = True

    def draw_trajectory(self, screen):
        if not self.launched:
            trajectory_color = (255, 255, 0)
            temp_pos = list(self.initial_pos)
            temp_velocity = list(self.velocity)

            for _ in range(15):
                temp_velocity[1] += self.gravity
                temp_pos[0] += temp_velocity[0]
                temp_pos[1] += temp_velocity[1]
                pygame.draw.circle(screen, trajectory_color, (int(temp_pos[0]), int(temp_pos[1])), 3)

    def check_collision(self, obstacle):
        if (self.pos[0] > obstacle.pos[0] and self.pos[0] < obstacle.pos[0] + obstacle.size[0] and
            self.pos[1] > obstacle.pos[1] and self.pos[1] < obstacle.pos[1] + obstacle.size[1]):
            return True
        return False
