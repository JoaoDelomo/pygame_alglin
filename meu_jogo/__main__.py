# meu_jogo/__main__.py
import pygame
import sys
from meu_jogo.game import Game
import os

def main():
    pygame.init()
    # Inicializar o mixer de som
    pygame.mixer.init()

    # Carregar e reproduzir a música de fundo
    caminho_musica = os.path.join(os.path.dirname(__file__), 'musica/musica.mp3')
    pygame.mixer.music.load(caminho_musica)
    pygame.mixer.music.play(-1)  # O argumento -1 faz com que a música toque em loop
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
