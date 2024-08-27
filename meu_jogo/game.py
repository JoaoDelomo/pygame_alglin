import pygame
import math
import os
from meu_jogo.button import CloseButton
from meu_jogo.projectile import Projectile
from meu_jogo.obstacle import Obstacle
from meu_jogo.gravity_center import GravityCenter
from meu_jogo.portal import Portal
from meu_jogo.goal import Goal

class Game:
    def __init__(self):
        pygame.init()

 

        self.screen_info = pygame.display.Info()
        self.width = self.screen_info.current_w
        self.height = self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.close_button = CloseButton(self.screen, self.width, self.height)

        # Carregar a imagem do background com caminho correto
        caminho = os.path.join(os.path.dirname(__file__), 'images/background.png')
        self.background = pygame.image.load(caminho).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Limite de projéteis
        self.max_projectiles = 10
        self.projectiles_remaining = self.max_projectiles

        self.projectile = Projectile((50, self.height - 50), self.width, self.height, size=50)
        self.gravity_center = GravityCenter((self.width // 2, self.height // 2), strength=500, influence_radius=100)
        self.portal = Portal()
        self.goal = Goal((1250, 500))

        self.running = True
        self.dragging = False
        self.portal_mode = 'entry'

        # Estado do jogo
        self.state = "start"

        # Única fase com obstáculos antes e depois do centro gravitacional
        self.obstacles = [
            Obstacle((self.width // 3, self.height - 150), (100, 50)),  # Obstáculo antes do centro gravitacional
            Obstacle((self.width // 3 * 2, self.height - 200), (100, 50))  # Obstáculo depois do centro gravitacional
        ]


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
            elif event.type == pygame.KEYDOWN:
                if self.state == "start":
                    if event.key == pygame.K_RETURN:
                        self.state = "instructions"
                elif self.state == "instructions":
                    if event.key == pygame.K_RETURN:
                        self.state = "playing"
                elif self.state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = "start"
                elif self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.place_portal(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button.is_clicked(event.pos):
                    self.running = False
                elif self.state == "playing":
                    if not self.projectile.launched and not self.dragging and self.projectiles_remaining > 0:
                        self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    if self.projectiles_remaining > 0:
                        self.projectile.launch()
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.calculate_power_and_angle(event.pos)

    def calculate_power_and_angle(self, mouse_pos):
        dx = mouse_pos[0] - self.projectile.initial_pos[0]
        dy = mouse_pos[1] - self.projectile.initial_pos[1]
        self.projectile.angle = math.degrees(math.atan2(-dy, dx))
        self.projectile.power = min(math.sqrt(dx**2 + dy**2) / 5, 50)
        self.projectile.calculate_velocity()

    def update(self):
        if self.state == "playing":
            # Atualizar a posição dos obstáculos
            for obstacle in self.obstacles:
                obstacle.move(self.screen)  # Passar a tela como argumento
            if self.projectile.launched:
                self.gravity_center.apply_gravity(self.projectile)
                self.portal.teleport(self.projectile)
                self.projectile.update()
                self.check_collisions()
                self.check_wall_collisions()  # Verificar colisões com as paredes

                if self.goal.check_collision(self.projectile):
                    print("Objetivo alcançado!")
                    self.state = "game_over"

    def draw(self):
        if self.state == "start":
            self.draw_start_screen()
        elif self.state == "instructions":
            self.draw_instructions_screen()
        elif self.state == "playing":
            self.draw_game_screen()
        elif self.state == "game_over":
            self.draw_game_over_screen()

        self.close_button.draw()

    def draw_start_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 74)
        text = font.render("Pressione Enter para Iniciar", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    def draw_instructions_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        instructions = [
            "Instruções:",
            "1. Use o mouse para mirar e definir a força.",
            "2. Pressione espaço para colocar o primeiro portal e depois para adicionar o segundo.",
            "3. Cuidado com os obstáculos!",
            "4. Você não pode colocar portais depois do centro gravitacional",
            "5. Alcance a casa do vizinho para ganhar.",
            "Pressione Enter para começar!"
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 200 + i * 50))

    def draw_game_screen(self):
        self.screen.blit(self.background, (0, 0))
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.gravity_center.draw(self.screen)
        self.portal.draw(self.screen)
        self.goal.draw(self.screen)
        if not self.projectile.launched:
            self.projectile.draw_trajectory(self.screen)
        self.projectile.draw(self.screen)

        # Desenhar contador de projéteis restantes
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Vidas restantes: {self.projectiles_remaining}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 74)
        text = font.render("Você venceu!", True, (0, 255, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
        text = font.render("Pressione Enter para reiniciar", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 + text.get_height()))

    def check_collisions(self):
        obstacles_to_remove = []
        for obstacle in self.obstacles:
            if self.projectile.check_collision(obstacle):
                if obstacle.hit():
                    obstacles_to_remove.append(obstacle)
                self.projectile.reset()
                self.reset_portals()  # Reinicia os portais quando o projétil colide com um obstáculo
                break
        for obstacle in obstacles_to_remove:
            self.obstacles.remove(obstacle)

    def check_wall_collisions(self):
        """Verifica colisões com as bordas da tela."""
        if (self.projectile.pos[0] - self.projectile.size <= 0 or 
            self.projectile.pos[0] + self.projectile.size >= self.width or
            self.projectile.pos[1] - self.projectile.size <= 0 or 
            self.projectile.pos[1] + self.projectile.size >= self.height):
            # Colidiu com a parede, resetar projétil e portais
            self.projectile.reset()
            self.reset_portals()
            self.projectiles_remaining -= 1
            print("Projétil colidiu com a parede. Resetando portais.")

    def place_portal(self, pos):
        if pos[0] > self.gravity_center.pos[0] +100:  # Verifica se a posição é depois do centro gravitacional
            print("Portais não podem ser colocados depois do campo gravitacional.")
            return
        
        if self.portal_mode == 'entry' and not self.portal.entry_placed:
            self.portal.set_entry(pos)
            self.portal_mode = 'exit'
        elif self.portal_mode == 'exit' and not self.portal.exit_placed:
            self.portal.set_exit(pos)
            self.portal_mode = 'none'

    def reset_game(self):
        """Reseta o estado do jogo para recomeçar."""
        self.projectile = Projectile((50, self.height - 50), self.width, self.height, size=50)
        self.reset_portals()  # Reinicia os portais ao resetar o jogo
        self.goal = Goal((1250, 100))
        self.projectiles_remaining = self.max_projectiles
        self.state = "start"
    
    def reset_portals(self):
        """Redefine a criação de portais."""
        self.portal = Portal()  # Cria uma nova instância para resetar os portais
        self.portal_mode = 'entry'
