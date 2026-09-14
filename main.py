"""Jogo educativo em Pygame: A* encontra um foco de dengue."""
from pathlib import Path
import math
import random
import pygame
from a_star import encontrar_caminho as executar_a_estrela
from greedy import encontrar_caminho as executar_gulosa

TILE, COLS, ROWS, PAINEL = 56, 16, 10, 104
WIDTH, HEIGHT, FPS = COLS * TILE, ROWS * TILE + PAINEL, 60
INICIO, DESTINO = (1, 1), (14, 8)
SEED_TEMPORARIA = 643922
ATLAS = {
    "G": (0, 0), "M": (1, 0), "T": (2, 0), "B": (3, 0),
    "C": (0, 1), "P": (1, 1), "baixo": (0, 2), "esquerda": (1, 2),
    "direita": (2, 2), "pneu": (3, 2),
}


def carregar_sprites():
    imagem = pygame.image.load(Path(__file__).parent / "assets" / "camping_spritesheet.png").convert_alpha()
    cw, ch = imagem.get_width() // 4, imagem.get_height() // 3
    return {nome: pygame.transform.scale(imagem.subsurface((col*cw, lin*ch, cw, ch)), (TILE, TILE))
            for nome, (col, lin) in ATLAS.items()}


def centro(tile):
    return pygame.Vector2(tile[0] * TILE + TILE / 2, tile[1] * TILE + TILE / 2)


def gerar_mapa_aleatorio():
    """Cria mapas aleatórios até o A* confirmar que um deles tem solução."""
    while True:
        seed = SEED_TEMPORARIA
        if seed is None:
            seed = random.SystemRandom().randrange(100_000, 1_000_000)
        sorteio = random.Random(seed)
        mapa = []

        for y in range(ROWS):
            linha = []
            for x in range(COLS):
                chance = sorteio.random()
                if chance < 0.18:
                    # Obstáculos variados do acampamento.
                    tile = sorteio.choice("TTTBBCCP")
                elif chance < 0.43:
                    tile = "M"
                else:
                    tile = "G"
                linha.append(tile)
            mapa.append(linha)

        # O início e o destino sempre precisam ser caminháveis.
        mapa[INICIO[1]][INICIO[0]] = "G"
        mapa[DESTINO[1]][DESTINO[0]] = "G"
        caminho, custo = executar_a_estrela(mapa, INICIO, DESTINO)
        if caminho is not None:
            return mapa, caminho, custo, seed


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Missão Dengue: A* ou Busca Gulosa")
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock, self.fonte = pygame.time.Clock(), pygame.font.Font(None, 27)
        self.fonte_p = pygame.font.Font(None, 21)
        self.sprites = carregar_sprites()
        self.algoritmo = None
        self.gerar_novo_mapa()

    def gerar_novo_mapa(self):
        self.mapa, _, _, self.seed = gerar_mapa_aleatorio()
        if self.algoritmo is None:
            self.caminho, self.custo = [], None
            self.reiniciar()
        else:
            self.selecionar_algoritmo(self.algoritmo)

    def selecionar_algoritmo(self, algoritmo):
        """Calcula uma nova rota sem alterar o mapa atual."""
        self.algoritmo = algoritmo
        if algoritmo == "A*":
            self.caminho, self.custo = executar_a_estrela(self.mapa, INICIO, DESTINO)
        else:
            self.caminho, self.custo = executar_gulosa(self.mapa, INICIO, DESTINO)
        self.reiniciar()

    def reiniciar(self):
        self.indice, self.posicao = 0, centro(INICIO)
        self.movendo = self.concluido = False
        self.direcao = "baixo"

    def atualizar(self, dt):
        if self.algoritmo is None or not self.movendo or self.concluido:
            return
        if self.indice == len(self.caminho) - 1:
            self.concluido, self.movendo = True, False
            return
        proximo = self.caminho[self.indice + 1]
        delta = centro(proximo) - self.posicao
        self.direcao = "esquerda" if delta.x < 0 else "direita" if delta.x > 0 else "baixo"
        # Lama também reduz visualmente a velocidade da criança.
        passo = (145 if self.mapa[proximo[1]][proximo[0]] == "G" else 82) * dt
        if delta.length() <= passo:
            self.posicao, self.indice = centro(proximo), self.indice + 1
        elif delta.length():
            self.posicao += delta.normalize() * passo

    def desenhar(self):
        # Limpa completamente o frame anterior. Alguns sprites possuem bordas
        # transparentes; sem esta limpeza, partes da criança poderiam continuar
        # visíveis entre um tile e outro, formando um "rastro".
        self.tela.fill((13, 29, 23))

        for y, linha in enumerate(self.mapa):
            for x, tipo in enumerate(linha):
                self.tela.blit(self.sprites[tipo if tipo in "GM" else "G"], (x*TILE, y*TILE))
                if tipo not in "GM":
                    self.tela.blit(self.sprites[tipo], (x*TILE, y*TILE))
        for i, tile in enumerate(self.caminho[1:-1], 1):
            pygame.draw.circle(self.tela, (255, 225, 75) if i >= self.indice else (255, 255, 255), centro(tile), 4)
        if not self.concluido:
            self.tela.blit(self.sprites["pneu"], (DESTINO[0]*TILE, DESTINO[1]*TILE))
        else:
            x, y = centro(DESTINO)
            pygame.draw.circle(self.tela, (36, 68, 55), (x, y), 18, 5)
            pygame.draw.lines(self.tela, (240, 255, 224), False, [(x-10, y), (x-2, y+9), (x+13, y-10)], 5)
        sprite = self.sprites[self.direcao]
        bob = math.sin(pygame.time.get_ticks()/100) * 2 if self.movendo else 0
        self.tela.blit(sprite, sprite.get_rect(center=(self.posicao.x, self.posicao.y+bob)))

        topo = ROWS * TILE
        pygame.draw.rect(self.tela, (24, 43, 36), (0, topo, WIDTH, PAINEL))
        titulo = "FOCO ELIMINADO! A água do pneu foi esvaziada." if self.concluido else "Missão: chegar ao pneu e eliminar a água parada"
        cor = (151, 238, 128) if self.concluido else (255, 240, 166)
        self.tela.blit(self.fonte.render(titulo, True, cor), (20, topo+13))
        if self.algoritmo is None:
            info = f"Aguardando seleção do algoritmo  •  mapa {self.seed}"
        else:
            info = f"{self.algoritmo} • custo: {self.custo}  |  grama: 1  •  lama: 3  |  {len(self.caminho)-1} passos  •  mapa {self.seed}"
        self.tela.blit(self.fonte_p.render(info, True, (225, 234, 224)), (20, topo+45))
        self.tela.blit(self.fonte_p.render("A: A*   G: Gulosa   ESPAÇO: iniciar/pausar   R: reiniciar   N: novo mapa", True, (177, 203, 185)), (20, topo+72))

        if self.algoritmo is None:
            sombra = pygame.Surface((WIDTH, ROWS*TILE), pygame.SRCALPHA)
            sombra.fill((7, 18, 14, 190))
            self.tela.blit(sombra, (0, 0))
            caixa = pygame.Rect(238, 174, 420, 212)
            pygame.draw.rect(self.tela, (28, 58, 45), caixa, border_radius=16)
            pygame.draw.rect(self.tela, (160, 218, 151), caixa, 3, border_radius=16)
            titulo_menu = self.fonte.render("Escolha o algoritmo de busca", True, (255, 245, 184))
            self.tela.blit(titulo_menu, titulo_menu.get_rect(center=(WIDTH//2, 220)))
            opcao_a = self.fonte.render("[ A ]  Busca A*", True, (235, 244, 232))
            opcao_g = self.fonte.render("[ G ]  Busca Gulosa", True, (235, 244, 232))
            self.tela.blit(opcao_a, opcao_a.get_rect(center=(WIDTH//2, 282)))
            self.tela.blit(opcao_g, opcao_g.get_rect(center=(WIDTH//2, 330)))

    def executar(self):
        rodando = True
        while rodando:
            dt = self.clock.tick(FPS) / 1000
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                    self.selecionar_algoritmo("A*")
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_g:
                    self.selecionar_algoritmo("Gulosa")
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE and self.algoritmo and not self.concluido:
                    self.movendo = not self.movendo
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    self.reiniciar()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_n:
                    self.gerar_novo_mapa()
            self.atualizar(dt)
            self.desenhar()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Jogo().executar()
