import pygame

class Obstacle:
    def __init__(self, pos, size, speed=2):
        self.pos = list(pos)
        self.size = list(size)
        self.speed = speed  # Velocidade vertical do obstáculo
        self.health = 3  # Cada obstáculo tem 3 pontos de vida

        # Carregar a imagem do obstáculo
        self.image = pygame.image.load("images/caixa.png").convert_alpha()  # Usar convert_alpha para suportar transparência
        self.image = pygame.transform.scale(self.image, self.size)  # Redimensionar a imagem para o tamanho do obstáculo

    def draw(self, screen):
        # Calcular a transparência baseada na vida restante
        transparency = max(0, 255 - (255 // 3) * (3 - self.health))
        # Criar uma cópia da imagem para aplicar a transparência
        transparent_image = self.image.copy()
        transparent_image.fill((255, 255, 255, transparency), None, pygame.BLEND_RGBA_MULT)

        # Desenhar a imagem transparente na tela
        screen.blit(transparent_image, self.pos)

    def move(self, screen):
        # Move o obstáculo para baixo
        self.pos[1] += self.speed

        # Inverte a direção ao atingir a parte inferior ou superior da tela
        if self.pos[1] <= 0 or self.pos[1] + self.size[1] >= screen.get_height():
            self.speed = -self.speed

    def hit(self):
        # Reduzir a vida do obstáculo ao ser atingido
        self.health -= 1
        if self.health <= 0:
            return True  # Indica que o obstáculo deve ser removido
        else:
            return False
