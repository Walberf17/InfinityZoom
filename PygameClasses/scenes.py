"""
default pygame template
"""

# import things
import pygame as pg, sys


# classes
class Scene:
    """
	this class will help to create diferent scenes for
	the games and apps.
	It creats a default loop:
		check if it stops,
		check events
		update things
		move things
		draw things
		update the display

	to run call --> self.run()
	to stop call --> self.stop()

	to do the things, creat a dict with the keys:
		"update , move , draw ,click_down , click_up
		key_down , key_up , multi_gesture".

		The values have to be a list of pg.groups|set|list.

		If no click_up is given , it will save the first object clicked
	and will click up only that object
	"""

    def __init__(self, screen_to_draw=None, dict_to_do=None, background="light blue", fps=45):
        """
		creates a scene object that has its own main loop.

		It needs a surface that will work with.

		It can take a dict of list with the objects to do things:
		to do the things, creat a dict with the keys:
			"update , move , draw ,click_down , click_up
		key_down , key_up , multi_gesture , finger_down , finger_up".

		exemple_dict = {
		'update': [],
		'move': [],
		'draw': [],
		'click_down': [],
		'click_up': [],
		'key_down': [],
		'key_up': [],
		'multi_gesture': [],
		'finger_down': [],
		'finger_up': []},
		'finger_motion' : []
		}

		:param screen_to_draw pg.Surface
		:param dicts_to_do dict object
		:param background pg.color
		:param FPS int
		"""

        if screen_to_draw is None:
            screen_to_draw = pg.display.set_mode(pg.display.get_desktop_sizes()[0], pg.FULLSCREEN)
        self.screen = screen_to_draw

        self.screen_rect = self.screen.get_rect()
        self.running = False
        self.FPS = fps
        self.obj_clicked = set()
        self.background = background
        self.to_update = list()
        self.to_move = list()
        self.to_draw = list()
        self.to_click_down = list()
        self.to_click_up = list()
        self.to_key_down = list()
        self.to_key_up = list()
        self.to_multi_gesture = list()
        self.to_finger_down = list()
        self.to_finger_up = list()
        self.to_finger_motion = list()
        self.set_things_to_do(dict_to_do=dict_to_do)
        self.create_objects()

    def run(self):
        """
		default loop.

		for it to stop call --> self.stop()

		It works in this order:
			check if stops
			events
			updates
			moves
			draws
			update pg display
		"""
        self.running = True
        clock = pg.time.Clock()
        while self.running:
            self.run_frame()
            pg.display.update()
            clock.tick(self.FPS)

    def run_frame(self):
        """
		Run 1 frame. It does not call the pygame.display.update()
		:return: None
		"""
        if pg.event.peek(pg.QUIT):
            self.quit()
        self.event_handler()
        self.update_handler()
        self.move_handler()
        self.draw_handler()

    def create_objects(self):
        """
        Change this class to create all the objects you will have in this class.
        :return:
        """
        pass

    def set_things_to_do(self, dict_to_do=None):
        if dict_to_do is None:
            dict_to_do = {}
        self.to_update = dict_to_do.get("update", [])
        self.to_move = dict_to_do.get("move", [])
        self.to_draw = dict_to_do.get("draw", [])
        self.to_click_down = dict_to_do.get("click_down", [])
        self.to_click_up = dict_to_do.get("click_up", [])
        self.to_key_down = dict_to_do.get("key_down", [])
        self.to_key_up = dict_to_do.get("key_up", [])
        self.to_multi_gesture = dict_to_do.get("multi_gesture", [])
        self.to_finger_down = dict_to_do.get("finger_down", [])
        self.to_finger_up = dict_to_do.get("finger_up", [])
        self.to_finger_motion = dict_to_do.get("finger_motion", [])

    def event_handler(self):
        """
		Default event handler.
		It calls the default handlers for given type of event.
		Default events:
			click_down_handler(event)
			click_up_handler(event)
			multi_gesture_handler(event)
			key_down_handler(event)
			key_up_handler(event)

		Change if needed.
		"""
        #	t = set()
        for event in pg.event.get():
            e_t = event.type  # get the type of the event
            if e_t == pg.MOUSEBUTTONDOWN:
                self.click_down_handler(event)
            elif e_t == pg.MOUSEBUTTONUP:
                self.click_up_handler(event)
            elif e_t == pg.MULTIGESTURE:
                self.multi_gesture_handler(event)
            elif e_t == pg.KEYDOWN:
                self.key_down_handler(event)
            elif e_t == pg.KEYUP:
                self.key_up_handler(event)
            elif e_t == pg.FINGERDOWN:
                self.finger_down_handler(event)
            elif e_t == pg.FINGERUP:
                self.finger_up_handler(event)
            elif e_t == pg.FINGERMOTION:
                self.finger_motion_handler(event)
            else:
                # print(event)
                pass

    def finger_motion_handler(self, event):
        for c_list in self.to_finger_motion:
            for obj in c_list:
                if obj.finger_motion(event):
                    self.obj_clicked.add(obj)
                    return

    def finger_down_handler(self, event):
        """
        Default finger down handler.
        Loops the objects in self.to_finger_down.
        It calls the default --> obj.finger_down(event).
        If the obj returns True, it stops the loop.
        If there is no objects in self.to_finger_down,
        It saves the object in a set with the clicked
        Objects in self.obj_clicked.
        Change if needed
        """
        for c_list in self.to_finger_down:
            for obj in c_list:
                if obj.finger_down(event):
                    self.obj_clicked.add(obj)
                    return

    def finger_up_handler(self, event):
        """
        param: pg.FINGERUP event
        Default finger up handler.
        Loops the objects in self.to_finger_up.
        It loops throught the objects in self.obj_clicked,
        then in self.to_finger_up, then if interacted with
        anything, it breaks the loop
        It calls the default --> obj.finger_up(event).
        Change if needed
        """
        if self.to_finger_up:
            # loops from self.obj_clicked
            for obj in self.obj_clicked:
                if obj.finger_up(event):
                    self.obj_clicked.clear()
                    return

            # loops if objects in self.to_finger_up
            for c_list in self.to_finger_up:
                for obj in c_list:
                    if obj.finger_up(event):
                        return
        else:
            for c_list in self.to_finger_down:
                for obj in c_list:
                    if obj.finger_up(event):
                        return

    def click_down_handler(self, event):
        """
        Default click down handler.
        Loops the objects in self.to_click_down.
        It calls the default --> obj.click_down(event).
        If the obj returns True, it stops the loop.
        It saves the object in a set with the clicked
        objects in self.obj_clicked.
        Change if needed
        """
        pg.mouse.get_rel()  # for smooth movement
        for c_list in self.to_click_down:
            for obj in c_list:
                if obj.click_down(event):
                    if not self.to_click_up:
                        self.obj_clicked.add(obj)
                    return

    def click_up_handler(self, event):
        """
        param: pg.MOUSEBUTTONUP event
        Default click up handler.
        Loops the objects in self.to_click_up.
        If there is no objects in self.to_click_up,
        it loops throught the objects in self.obj_clicked.
        It calls the default --> obj.click_up(event).
        Change if needed
        """

        # loops from self.obj_clicked
        for obj in self.obj_clicked:
            if obj.click_up(event):
                self.obj_clicked.clear()
                return

        # loops if objects in self.to_click_up
        if self.to_click_up:
            for c_list in self.to_click_up:
                for obj in c_list:
                    obj.click_up(event)


        # loops from self.obj_clicked
        else:
            for c_list in self.to_click_down:
                for obj in c_list:
                    obj.click_up(event)

    def multi_gesture_handler(self, event):
        """
        Default multi_gesture_handler.
        For touch devices
        Loops throught self.to_multi_gesture and
        calls --> obj.multi_gesture(event)
        """
        for c_list in self.to_multi_gesture:
            for obj in c_list:
                obj.multi_gesture(event)

    def key_down_handler(self, event):
        """
        Default press key handler.
        Loops through self.to_key_down and
        calls --> obj.key_down(event)
        """
        pg.mouse.get_rel()  # for smooth movement
        for c_list in self.to_key_down:
            for obj in c_list:
                obj.key_down(event)

    def key_up_handler(self, event):
        """
        Default press key handler.
        Loops throught self.to_key_up and
        calls --> obj.key_up(event)
        """
        for c_list in self.to_key_up:
            for obj in c_list:
                obj.key_up(event)

    def update_handler(self):
        """
        Default press key handler.
        Loops throught self.to_update and
        calls --> obj.update()
        """
        # pg.mouse.get_rel()
        for c_list in self.to_update:
            for obj in c_list:
                obj.update()

    def move_handler(self):
        """
        Default move handler.
        Loops throught self.to_move and
        calls --> obj.move()
        """
        # pg.mouse.get_rel()
        for c_list in self.to_move:
            for obj in c_list:
                obj.move()

    def draw_handler(self):
        """
        Default draw handler.
        Loops throught self.to_draw and
        calls --> obj.draw(self.screen)
        It fills the screen with the self.background color.
        Than draws the things, then updates the display.
        """

        self.screen.fill(self.background)
        for c_list in self.to_draw:
            for obj in c_list:
                obj.draw(self.screen)

    def run_other(self, scene):
        """
        Starts other scene.
        :param scene: A Scene object
        :return: None
        """
        if type(scene) == type:
            scene().run()
        else:
            scene.run()

    def stop_other(self, scene):
        """
        Stops other scene.
        :param scene: A Scene object
        :return: None
        """
        if type(scene) == type:
            scene().stop()
        else:
            scene.stop()

    def stop(self):
        self.running = False

    def quit(self):
        pg.quit()
        sys.exit()


class Canvas:
    def __init__(self):
        self.points = list()
        self.creating = False

    def finger_down(self, event):
        pos = pg.Vector2(event.x, event.y)
        self.creating = True
        for pt in self.points:
            if pos.distance_to(pt) <= 30:
                self.creating = False
                break
        if self.creating:
            self.points.append(event.pos)

    def finger_up(self, event):
        if not self.creating:
            to_remove = set()
            pos = pg.Vector2(event.x, event.y)
            for pt in self.points:
                if pos.distance_to(pt) <= 30:
                    to_remove.add(pt)
            for pt in to_remove:
                self.points.remove(pt)
        else:
            self.creating = False

    def click_down(self, event):
        pos = pg.Vector2(event.pos)
        self.creating = True
        for pt in self.points:
            if pos.distance_to(pt) <= 30:
                self.creating = False
                break
        if self.creating:
            self.points.append(event.pos)

    def click_up(self, event):
        if not self.creating:
            to_remove = set()
            pos = pg.Vector2(event.pos)
            for pt in self.points:
                if pos.distance_to(pt) <= 30:
                    to_remove.add(pt)
            for pt in to_remove:
                self.points.remove(pt)
        else:
            self.creating = False

    def update(self):
        if self.creating:
            self.points[-1] = pg.mouse.get_pos()

    def draw(self, screen_to_draw):
        for x, y in self.points:
            pg.draw.line(screen_to_draw, "red", (x, 0), (x, screen_rect.h), 6)
            pg.draw.line(screen_to_draw, "red", (0, y), (screen_rect.w, y), 6)


# run
if __name__ == "__main__":
    screen = pg.display.set_mode((400, 800))
    screen_rect = screen.get_rect()
    a = Canvas()
    main_menu = Scene(screen, dict_to_do={"finger_down": [[a]], 'update': [[a]], "draw": [[a]], "finger_up": [[a]],
                                          'click_down': [[a]]})
    main_menu.run()
