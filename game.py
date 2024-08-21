import pygame
import json
from button import CloseButton
from projectile import Projectile
from obstacle import Obstacle
from gravity_center import GravityCenter
from portal import Portal
from goal import Goal
import math

class Game:
    def __init__(self):
        self.screen_info = pygame.display.Info()
        self.width = self.screen_info.current_w
        self.height = self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.close_button = CloseButton(self.screen, self.width, self.height)

        # Carregar a imagem do background
        self.background = pygame.image.load("images/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Limite de projéteis
        self.max_projectiles = 5
        self.projectiles_remaining = self.max_projectiles

        self.projectile = Projectile((50, self.height - 50), self.width, self.height, size=50)

        self.obstacles = [
            Obstacle((self.width // 2, self.height - 150), (100, 50)),
            Obstacle((self.width // 2 + 120, self.height - 200), (100, 50))
        ]

        self.gravity_center = GravityCenter((self.width // 2, self.height // 2), strength=500, influence_radius=100)

        self.portal = Portal()

        self.goal = Goal((700, 100))  # Posição do objetivo

        self.running = True
        self.dragging = False
        self.portal_mode = 'entry'  # Primeiro clique define a entrada

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button.is_clicked(event.pos):
                    self.running = False
                elif not self.projectile.launched and not self.dragging and self.projectiles_remaining > 0:
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    if self.projectiles_remaining > 0:
                        self.projectile.launch()
                        self.projectiles_remaining -= 1
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.calculate_power_and_angle(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.place_portal(pygame.mouse.get_pos())  # Coloca o portal na posição do mouse

    def calculate_power_and_angle(self, mouse_pos):
        dx = mouse_pos[0] - self.projectile.initial_pos[0]
        dy = mouse_pos[1] - self.projectile.initial_pos[1]
        self.projectile.angle = math.degrees(math.atan2(-dy, dx))
        self.projectile.power = min(math.sqrt(dx**2 + dy**2) / 5, 50)
        self.projectile.calculate_velocity()

    def update(self):
        if self.projectile.launched:
            self.gravity_center.apply_gravity(self.projectile)
            self.portal.teleport(self.projectile)
            self.projectile.update()
            self.check_collisions()

            # Verificar se o projétil atingiu o objetivo
            if self.goal.check_collision(self.projectile):
                print("Objetivo alcançado!")
                self.running = False

    def draw(self):
        # Desenhar o background
        self.screen.blit(self.background, (0, 0))

        self.close_button.draw()
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.gravity_center.draw(self.screen)
        self.portal.draw(self.screen)
        self.goal.draw(self.screen)  # Desenhar o objetivo
        if not self.projectile.launched:
            self.projectile.draw_trajectory(self.screen)
        self.projectile.draw(self.screen)

        # Desenhar contador de projéteis restantes
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Projéteis restantes: {self.projectiles_remaining}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def check_collisions(self):
        obstacles_to_remove = []
        
        for obstacle in self.obstacles:
            if self.projectile.check_collision(obstacle):
                if obstacle.hit():
                    obstacles_to_remove.append(obstacle)
                self.projectile.reset()
                break

        for obstacle in obstacles_to_remove:
            self.obstacles.remove(obstacle)

    def place_portal(self, pos):
        """Posiciona os portais de entrada e saída uma vez."""
        if self.portal_mode == 'entry' and not self.portal.entry_placed:
            self.portal.set_entry(pos)
            self.portal_mode = 'exit'
        elif self.portal_mode == 'exit' and not self.portal.exit_placed:
            self.portal.set_exit(pos)
            self.portal_mode = 'none'  # Depois de colocar ambos os portais, desativa a colocação
