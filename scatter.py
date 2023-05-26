import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from PygameClasses.buttons import Button
from functools import partial
from PygameClasses.textbox import TextBox
from pygame.sprite import Group


# Variables


# Helpers
def calc_proportional_size(expected=None, max_area=(1, 1), max_rect=None):
    """
	It calculates a proportional thing to the given rect and max size, given in units.
	The max size is the proportion, max size of the rect, in units.
	:param expected: a list or tuple with the size in meters
	:param max_area: a list with the max are of the thing that you want to compare
	:param max_rect: pygame.Rect, the rect that you want to compare
	:return:
	"""
    if max_rect is None:
        raise EOFError(f'Max rect not found')
    max_sizes = pg.Vector2(max_rect.size)
    proportion = max_sizes.elementwise() / max_area

    if expected is None:
        expected = [1, 1]

    if type(expected) in [float, int]:
        return proportion[1] * expected
    elif len(expected) == 2:
        return proportion.elementwise() * expected
    elif len(expected) == 4:
        pos = proportion.elementwise() * expected[:2] + max_rect.topleft
        size = proportion.elementwise() * expected[2:]
        return [pos, size]
    else:
        raise TypeError(f'value not good enought, {expected}')


# main classes

class Scatter:

    def __init__(self, area, x_lim, resolution, rect_to_be, center=(.5, .5), pt_color='black', pt_size=1, xs=100):
        self.xs = xs
        self.x_lim = x_lim
        self.y_lim = None
        self.initial_x_lim = x_lim
        self.resolution = resolution
        self.rect = pg.Rect([0, 0], calc_proportional_size(area, max_rect=rect_to_be))
        self.rect.center = calc_proportional_size(center, max_rect=rect_to_be)
        self.graph = pg.Surface(self.rect.size).convert_alpha()
        self.area = area
        self.x = 0
        self.r = 0
        self.points = list()
        self.xs = list()
        self.rs = list()
        # self.init_chaos(new_x=.8, new_r=3.99, iters=400)
        self.pt_size = pt_size
        self.pt_color = pt_color
        self.create_points()
        self.clicked = False
        self.mark_down = list()
        self.texts = Group()
        self.buttons = Group()
        Button((.1, .1), [0.1, -.05], rect_to_be=self.rect, text='Zoom',
               on_click_up=partial(self.set_limits, self.initial_x_lim, None), groups=self.buttons)
        self.max_y = TextBox('{0:.2f}'.format(max(self.y_lim)), area=[-.05, .05], rect_to_be=self.rect,
                             relative_center=[-.07, -0], groups=[self.texts],
                             bg_color=None, font_color='black')
        self.min_y = TextBox('{0:.2f}'.format(min(self.y_lim)), area=[-.05, .05], rect_to_be=self.rect,
                             relative_center=[-.07, 1], groups=[self.texts],
                             bg_color=None, font_color='black')
        self.max_x = TextBox('{0:.2f}'.format(max(self.x_lim)), area=[-.05, .05], rect_to_be=self.rect,
                             relative_center=[1, 1.05], groups=[self.texts],
                             bg_color=None, font_color='black')
        self.min_x = TextBox('{0:.2f}'.format(min(self.x_lim)), area=[-.05, .05], rect_to_be=self.rect,
                             relative_center=[0, 1.05], groups=[self.texts],
                             bg_color=None, font_color='black')

    def create_points(self):
        self.points.clear()
        array = list()
        for r in np.linspace(min(self.x_lim), max(self.x_lim), self.resolution):
            self.init_chaos(new_x=.2, new_r=r, iters=400)
            new_array = self.create_array_bifurcation(100)
            for x in np.unique(new_array):
                array.append([r, x])
        array = np.array(array)
        if self.y_lim is None:
            self.y_lim = [array[:, 1].min(), array[:, 1].max()]

        for pt in array:
            self.points.append(self.calc_position(pt))

        self.draw_graph()

    def draw_graph(self):
        self.graph.fill([0, 0, 0, 0])
        for pt in self.points:
            pg.draw.circle(self.graph, self.pt_color, pt, self.pt_size)

        # # zeros
        # zeros = self.calc_position((0,0))
        # # if self.rect.collidepoint(pg.Vector2(zeros)-self.rect.topleft):
        # # draw y
        # pg.draw.line(self.graph, 'black', [zeros[0],0], [zeros[0],self.rect.h])
        #
        # pg.draw.line(self.graph, 'black', [0, zeros[1]], [self.rect.w, zeros[1]])

    def create_array_bifurcation(self, size):
        array = list()

        counter = 0

        while len(array) <= size and counter <= size * 50:
            counter += 1
            self.logistic_map_once()

            if self.y_lim is None:
                array.append(self.x)
            elif min(self.y_lim) <= self.x <= max(self.y_lim):
                array.append(self.x)

        array = np.array(array)
        return array

    def set_x_r_logistic(self, new_x=None, new_r=None):
        if new_x is not None:
            self.x = new_x
        if new_r is not None:
            self.r = new_r

    def init_chaos(self, new_x, new_r, iters):
        self.set_x_r_logistic(new_x, new_r)
        self.iter_logistic(iters)

    def iter_logistic(self, iters):
        for _ in range(iters):
            self.logistic_map_once()

    def logistic_map_once(self):
        self.x = self.x * self.r * (1 - self.x)

    def calc_position(self, pt):
        im_x, im_y = list(pt)
        im_y = max(self.y_lim) - im_y

        dist_im_x = abs(self.x_lim[0] - self.x_lim[1])
        dist_im_y = abs(self.y_lim[0] - self.y_lim[1])

        dist_r_x, dist_r_y = self.rect.size

        dx = dist_r_x * (im_x - min(self.x_lim)) / dist_im_x
        dy = (dist_r_y * im_y / dist_im_y) + max(self.y_lim)

        # return pg.Vector2(dx, dy)+self.rect.topleft
        return dx, dy

    def draw(self, screen_to_draw):
        pg.draw.rect(screen_to_draw, 'red', self.rect, 1)

        screen_to_draw.blit(self.graph, self.rect)

        mouse_pos = pg.mouse.get_pos()

        for btn in self.buttons:
            btn.draw(screen_to_draw)

        for txt in self.texts:
            txt.draw(screen_to_draw)

        if self.clicked and self.mark_down and self.rect.collidepoint(mouse_pos):
            # draw the first mark
            pg.draw.line(screen_to_draw, 'black', [self.mark_down[0][0], self.rect.top],
                         [self.mark_down[0][0], self.rect.bottom])
            pg.draw.line(screen_to_draw, 'black', [self.rect.left, self.mark_down[0][1]],
                         [self.rect.right, self.mark_down[0][1]])

            # draw the mouse position

            pg.draw.line(screen_to_draw, 'black', [mouse_pos[0], self.rect.top], [mouse_pos[0], self.rect.bottom])
            pg.draw.line(screen_to_draw, 'black', [self.rect.left, mouse_pos[1]], [self.rect.right, mouse_pos[1]])

    def click_down(self, event):
        for btn in self.buttons:
            if btn.click_down(event):
                return True

        if self.rect.collidepoint(event.pos):
            self.clicked = True
            self.mark_down.append(pg.Vector2(event.pos))
        return self.clicked

    def click_up(self, event):
        for btn in self.buttons:
            if btn.click_up(event):
                return True
        if self.clicked and self.rect.collidepoint(event.pos):
            self.mark_down.append(pg.Vector2(event.pos))
            self.get_limits()
            self.mark_down.clear()
            return True
        else:
            self.mark_down.clear()

    def get_limits(self):
        [[x1, y1], [x2, y2]] = self.mark_down

        dist_im_x = abs(self.x_lim[0] - self.x_lim[1])
        dist_im_y = abs(self.y_lim[0] - self.y_lim[1])

        dist_r_x, dist_r_y = self.rect.size

        dx_1 = dist_im_x * (x1 - self.rect.left) / dist_r_x
        dx_2 = dist_im_x * (x2 - self.rect.left) / dist_r_x

        dy_1 = dist_im_y * (y1 - self.rect.top) / dist_r_y
        dy_2 = dist_im_y * (y2 - self.rect.top) / dist_r_y

        lim_x = [dx_1 + min(self.x_lim), dx_2 + min(self.x_lim)]
        lim_y = [max(self.y_lim) - dy_1, max(self.y_lim) - dy_2]
        lim_x.sort()
        lim_y.sort()

        if pg.Vector2(x1, y1).distance_to([x2, y2]) > 30:
            self.set_limits(lim_x, lim_y)

    def set_limits(self, lim_x, lim_y):
        self.x_lim = lim_x
        self.y_lim = lim_y
        self.create_points()
        self.update_text_limites()

    def update_text_limites(self):
        min_y, max_y = self.y_lim
        min_x, max_x = self.x_lim

        self.min_y.change_text('{0:.4f}'.format(min_y))
        self.max_y.change_text('{0:.4f}'.format(max_y))

        self.min_x.change_text('{0:.4f}'.format(min_x))
        self.max_x.change_text('{0:.4f}'.format(max_x))
