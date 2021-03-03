import random
import pygame
import sys
from configparser import ConfigParser
import ctypes

BOARD_SIZE = WIDTH, HEIGHT = 860, 600
CELL_SIZE = 10
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 255
RED = 0, 255, 0
MAX_FPS = 9


class ConwayGame:
    """"
    INITIAL FUNCTIONS
    {def init} and {def run}

    Two main functions:
        def init ==> inicializa a classe
        def run ==> roda o game loop

    """

    def __init__(self):
        pygame.init()
        self.config()
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        self.atualiza_tela()
        pygame.display.flip()

        self.grid_ativa = 0
        self.n_cols = int(WIDTH / CELL_SIZE)
        self.n_lins = int(HEIGHT / CELL_SIZE)
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.pause = False
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            if self.game_over:
                return

            self.eventos()

            if not self.pause:
                self.atualiza_geracao()
                self.desenha_grid()

            clock.tick(MAX_FPS)

    def config(self):

        config = ConfigParser()
        config.read(R"configs\config.ini")

        pygame.display.set_caption(config['GAME_CONFIGS']['titile'])

        print(config['GAME_CONFIGS']['icon'])

        icon = pygame.image.load(config['GAME_CONFIGS']['icon'])
        pygame.display.set_icon(icon)

        pygame.mixer.music.load(config['GAME_CONFIGS']['music'])
        pygame.mixer.music.play(-1, 0.0)

        myappid = config['GAME_CONFIGS']['icon']  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        bg = pygame.image.load(config['GAME_CONFIGS']['background'])
        tela = pygame.display.set_mode((WIDTH, HEIGHT))
        tela.blit(bg, (0, 0))

    # ==================================================================================================================

    """"

    GRID FUNCTIONS
    {def init_grids}, {def create_grid}, {def set_grid} and {def draw_grid}

    Four grids functions:
        def init_grids ==> inicializa e cria as grids
        def set_grid ==> define os valores das celulas
        def desenha_grid ==> define as cores e desenhas as celulas
        def grid_inativa ==> retorna a grid inativa

    """

    def init_grids(self):

        def cria_grid():
            linhas = []
            for n_linha in range(self.n_lins):
                lista_colunas = [0] * self.n_cols
                linhas.append(lista_colunas)
            return linhas

        self.grids.append(cria_grid())
        self.grids.append(cria_grid())

    def set_grid(self, value=None, grid=0):
        for r in range(self.n_lins):
            for c in range(self.n_cols):
                if value is None:
                    valor_da_cell = random.randint(0, 1)
                else:
                    valor_da_cell = value
                self.grids[grid][r][c] = valor_da_cell

    def desenha_grid(self):
        self.atualiza_tela()
        for c in range(self.n_cols):
            for r in range(self.n_lins):
                if self.grids[self.grid_ativa][r][c] == 1:
                    cor = random.choice([ALIVE_COLOR, RED])
                else:
                    cor = DEAD_COLOR
                pygame.draw.circle(self.tela,
                                   cor,
                                   (int(c * CELL_SIZE + (CELL_SIZE / 2)),
                                    int(r * CELL_SIZE + (CELL_SIZE / 2))),
                                   int(CELL_SIZE / 2),
                                   0)
        pygame.display.flip()

    def grid_inativa(self):
        return (self.grid_ativa + 1) % 2

    # ==================================================================================================================

    """"

    GAME FUNCTIONS
    {def eventos} and {def atualiza_tela}

    Two game functions:
        def eventos ==> lida com os eventos do jogo, como sair, pausar e randomizar a grid novamente
        def atualiza_tela ==> atualiza a tela

    """

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("Tecla pressionada <-->")
                if event.unicode == 's':
                    print("Jogo pausado.")
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif event.unicode == 'r':
                    print("Grid randomizada.")
                    self.grid_ativa = 0
                    self.set_grid(None, self.grid_ativa)
                    self.set_grid(0, self.grid_inativa())
                    self.desenha_grid()
                elif event.unicode == 'q':
                    print("Game fechado.")
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def atualiza_tela(self):
        config = ConfigParser()
        config.read(R"configs\config.ini")

        bg = pygame.image.load(R"C:\ws-py\ConwaysLifeGame\configs\backgrounbd_image.png")
        self.tela.blit(bg, (0, 0))

    # ==================================================================================================================

    """"

    CELLS FUNCTIONS
    {def valor_cell}, {def check_redor_da_cell} and {def atualiza_geracao}

    Three cell functions:
        def valor_cell ==> pega o valor atual da celula
        def check_redor_da_cell ==> check as regras do jogo, vendo as celulas ao lado da ativa
        def atualiza_geracao ==> faz o update da grid e as novas geracoes de celulas.

    """

    def valor_cell(self, row_num, col_num):

        try:
            cell_value = self.grids[self.grid_ativa][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_redor_da_cell(self, r, c):

        vizinhos_da_cell = 0
        vizinhos_da_cell += self.valor_cell(r - 1, c - 1)
        vizinhos_da_cell += self.valor_cell(r - 1, c)
        vizinhos_da_cell += self.valor_cell(r - 1, c + 1)
        vizinhos_da_cell += self.valor_cell(r, c - 1)
        vizinhos_da_cell += self.valor_cell(r, c + 1)
        vizinhos_da_cell += self.valor_cell(r + 1, c - 1)
        vizinhos_da_cell += self.valor_cell(r + 1, c)
        vizinhos_da_cell += self.valor_cell(r + 1, c + 1)

        if self.grids[self.grid_ativa][r][c] == 1:
            if vizinhos_da_cell > 3:
                return 0
            if vizinhos_da_cell < 2:
                return 0
            if vizinhos_da_cell == 2 or vizinhos_da_cell == 3:
                return 1
        elif self.grids[self.grid_ativa][r][c] == 0:
            if vizinhos_da_cell == 3:
                return 1

        return self.grids[self.grid_ativa][r][c]

    def atualiza_geracao(self):
        for r in range(self.n_lins - 1):
            for c in range(self.n_cols - 1):
                proximo_estado_gen = self.check_redor_da_cell(r, c)
                self.grids[self.grid_inativa()][r][c] = proximo_estado_gen
        self.grid_ativa = self.grid_inativa()

    # ==================================================================================================================


""""

    RUN CODE :)

"""

if __name__ == '__main__':
    game = ConwayGame()
    game.run()
