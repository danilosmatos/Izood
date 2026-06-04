import pygame

class ContadorDePassosJogo:
    def __init__(self):
        self.passos_efetuados = 0

    def registrar_passo(self):
        """Incrementa o contador a cada movimento validado."""
        self.passos_efetuados += 1

    def zerar_contador(self):
        self.passos_efetuados = 0

  # UI simplesdo contador  
    def desenhar_contador(self, tela, x=20, y=20):
        """Desenha o contador de passos principal do gameplay na tela."""
        fonte = pygame.font.SysFont(None, 30)
        texto = fonte.render(f"Passos Dados: {self.passos_efetuados}", True, (255, 255, 0)) # Amarelo
        tela.blit(texto, (x, y))
