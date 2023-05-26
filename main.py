"""
This app will zoom infinitely into a graph, creating an ever-increasing zoom for the equation

For now only the Logistic Map, in the r by x values

"""

from PygameClasses.scenes import Scene
from scatter import Scatter
import pygame as pg

# variables
# cor de fundo: colocar uma cor que o pygame reconhece, no estilo [r,g,b] ou nome da cor em inglês
cor_de_fundo = 'white'

# cor dos pontos no gráfico: colocar uma cor que o pygame reconhece, no estilo [r,g,b] ou nome da cor em inglês
cor_pt = 'red'

# Tamanho do ponto: in valor inteiro para o tamanho do ponto.
tamanho_pt = 1

# Resolução: inteiro com o número de pontos em r que ele procura (eixo x)
resolution = 1000

# xs = número de valores de x que ele procura em cada ponto de r
xs = 100

# helpers


# classes
screen = pg.display.set_mode([900, 800])

scat = Scatter(area=[.8, .8], x_lim=[-2, 4], resolution=resolution, rect_to_be=screen.get_rect(), center=(.55, .5),
               pt_color=cor_pt, pt_size=tamanho_pt, xs=xs)

a = Scene(screen, dict_to_do={'draw': [[scat]], 'click_down': [[scat]]}, background=cor_de_fundo)
a.run()
# tests
