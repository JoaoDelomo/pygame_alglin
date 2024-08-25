import pygame

class Portal:
    def __init__(self):
        self.entry_pos = None  # Posição do portal de entrada (azul)
        self.exit_pos = None  # Posição do portal de saída (laranja)
        self.radius = 20  # Raio visual do portal
        self.entry_placed = False  # Indicador se o portal de entrada foi colocado
        self.exit_placed = False  # Indicador se o portal de saída foi colocado
        self.cooldown = 0  # Tempo de cooldown para evitar teletransporte repetido

        # Carregar as imagens dos portais
        self.entry_image = pygame.image.load('images/portal_azul.png')
        self.exit_image = pygame.image.load('images/portal_laranja.png')

        # Ajustar o tamanho das imagens para corresponder ao raio definido
        self.entry_image = pygame.transform.scale(self.entry_image, (self.radius * 2, self.radius * 2))
        self.exit_image = pygame.transform.scale(self.exit_image, (self.radius * 2, self.radius * 2))

    def set_entry(self, pos):
        """Define a posição do portal de entrada se ele ainda não foi colocado."""
        if not self.entry_placed:
            self.entry_pos = pos
            self.entry_placed = True  # Marca que o portal de entrada foi colocado

    def set_exit(self, pos):
        """Define a posição do portal de saída se ele ainda não foi colocado."""
        if not self.exit_placed:
            self.exit_pos = pos
            self.exit_placed = True  # Marca que o portal de saída foi colocado

    def draw(self, screen):
        """Desenha os portais na tela."""
        if self.entry_pos:
            # Desenha o portal de entrada (azul)
            screen.blit(self.entry_image, (self.entry_pos[0] - self.radius, self.entry_pos[1] - self.radius))
        if self.exit_pos:
            # Desenha o portal de saída (laranja)
            screen.blit(self.exit_image, (self.exit_pos[0] - self.radius, self.exit_pos[1] - self.radius))

    def teleport(self, projectile):
        """Teletransporta o projétil entre os portais."""
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if self.entry_pos and self.exit_pos:
            dist_to_entry = self._distance(self.entry_pos, projectile.pos)
            dist_to_exit = self._distance(self.exit_pos, projectile.pos)

            if dist_to_entry < self.radius:
                # Teletransporta do azul para o laranja
                offset_x = projectile.pos[0] - self.entry_pos[0]
                offset_y = projectile.pos[1] - self.entry_pos[1]
                projectile.pos = [self.exit_pos[0] + offset_x, self.exit_pos[1] + offset_y + self.radius + 1]  # Move o projétil para fora do raio de colisão
                projectile.velocity[1] = abs(projectile.velocity[1])  # Sair descendo
                self.cooldown = 10  # Impede a colisão imediata após o teletransporte

            elif dist_to_exit < self.radius:
                # Teletransporta do laranja para o azul
                offset_x = projectile.pos[0] - self.exit_pos[0]
                offset_y = projectile.pos[1] - self.exit_pos[1]
                projectile.pos = [self.entry_pos[0] + offset_x, self.entry_pos[1] + offset_y + self.radius + 1]  # Move o projétil para fora do raio de colisão
                projectile.velocity[1] = abs(projectile.velocity[1])  # Sair descendo
                self.cooldown = 10  # Impede a colisão imediata após o teletransporte

    def _distance(self, pos1, pos2):
        """Calcula a distância entre dois pontos."""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
